from clang import cindex

import samo_tidy.checker.checker as checker

ID = "TIDY_SAMO_MISSING_CONST"


def hash(token):
    """Hash the location to be used in the set"""
    return f"{token.location.file.name}:{token.location.line}:{token.location.column}"


def print_references():
    """Debug output"""
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.DECL_REF_EXPR:
            if token.referenced:
                print(
                    f"The token {token.kind} in {dump.pretty_location(token.location)} as definition={token.is_definition()} is used"
                )
                for reference in token.referenced.walk_preorder():
                    print(
                        f"\tby token {reference.kind} in {dump.pretty_location(reference.location)} as definition={reference.is_definition()}"
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
        if (
            token.kind == cindex.CursorKind.BINARY_OPERATOR
            or token.kind == cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR
        ):
            for child in token.get_children():
                if child.kind == cindex.CursorKind.DECL_REF_EXPR:
                    if child.referenced:
                        for reference in child.referenced.walk_preorder():
                            if reference.kind == cindex.CursorKind.VAR_DECL:
                                all_non_const_variable_declarations[hash(reference)] = None

    # Create violations based on non-const read-only variables
    for _, the_used_token in all_non_const_variable_declarations.items():
        if the_used_token:
            violation = checker.extract_violation(
                the_used_token,
                ID,
                f"The variable {the_used_token.spelling} could be made const",
            )
            if violation:
                violations.append(violation)

    return violations
