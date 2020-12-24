from clang import cindex
import logging

import samo_tidy.checker.checker as checker
import samo_tidy.dump.dump as dump


ID = "TIDY_SAMO_MISSING_CONST"


def check_references(token):
    """Check whether a variable definition is used as a reference in a function"""
    if token.kind == cindex.CursorKind.CALL_EXPR:
        for child in token.get_children():
            # Important is the difference between CursorKind.UNEXPOSED_EXPR and CursorKind.DECL_REF_EXPR.
            # Only the latter indicates that a reference is directly used.
            if child.kind == cindex.CursorKind.DECL_REF_EXPR:
                if child.referenced:
                    for reference in child.referenced.walk_preorder():
                        if reference.kind == cindex.CursorKind.VAR_DECL:
                            return reference
    return None


def fix_rule(violated_line, violation):
    first_part = get_substring_from_list(violated_line, 0, violation.column - 1)
    second_part = get_substring_from_list(violated_line, violation.column - 1, len(violated_line))
    fixed_line = f"{first_part}const {second_part}"
    return fixed_line


def get_substring_from_list(line, start, end):
    return "".join(line[start:end])


def hash(token):
    """Hash the location to be used in the set"""
    return f"{token.location.file.name}:{token.location.line}:{token.location.column}"


def helpful_debug_output():
    print_references(translation_unit, kind=cindex.CursorKind.DECL_REF_EXPR, name="change_me")
    print_references(translation_unit, kind=cindex.CursorKind.CALL_EXPR, name="Change")


def print_references(translation_unit, kind=None, name=None):
    """Debug output"""
    for token in translation_unit.cursor.walk_preorder():
        if kind:
            if token.kind != kind:
                continue
        if name:
            if token.spelling != name:
                continue
        if token.referenced:
            print(
                f"The token '{token.kind}' named '{token.spelling}' in '{dump.pretty_location(token.location)}'"
                f"as definition={token.is_definition()} is used"
            )
            for reference in token.referenced.walk_preorder():
                print(
                    f"\tby token '{reference.kind}' named '{reference.spelling}' in '{dump.pretty_location(reference.location)}'"
                    f"as definition={reference.is_definition()}"
                )


def translation_unit_based_rule(translation_unit):
    """Find variable declrations which could be made const"""
    # TODO Check usage of a variable when handing over as a non-const reference
    violations = []

    # All non-const variable declaration are suspected to be read-only
    all_non_const_variable_declarations = {}
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.VAR_DECL:
            if not token.type.is_const_qualified():
                all_non_const_variable_declarations[hash(token)] = token

    # Check which of those variable declarations are being used as a reference in a binary operation (:= written)
    for token in translation_unit.cursor.walk_preorder():
        referenced = check_references(token)
        if referenced:
            all_non_const_variable_declarations[hash(referenced)] = None
        if (
            token.kind == cindex.CursorKind.BINARY_OPERATOR
            or token.kind == cindex.CursorKind.UNARY_OPERATOR
            or token.kind == cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR
        ):
            for child in token.get_children():
                if child.kind == cindex.CursorKind.DECL_REF_EXPR:
                    if child.referenced:
                        for reference in child.referenced.walk_preorder():
                            if reference.kind == cindex.CursorKind.VAR_DECL:
                                all_non_const_variable_declarations[hash(reference)] = None

    # Create violations based on non-const read-only variables
    # If the used token is not None, we have a violation
    for _, the_used_token in all_non_const_variable_declarations.items():
        if the_used_token:
            violation = checker.extract_violation(
                the_used_token,
                ID,
                f"The variable '{the_used_token.spelling}' could be made const",
            )
            if violation:
                violations.append(violation)
    return violations
