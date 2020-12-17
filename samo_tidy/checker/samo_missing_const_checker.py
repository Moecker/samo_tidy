from clang import cindex

import samo_tidy.checker.checker as checker
import samo_tidy.dump.dump as dump


def hash(token):
    return f"{token.location.line}:{token.location.column}"


def playground():
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
    violations = []

    all_var_decls = {}
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.VAR_DECL:
            all_var_decls[hash(token)] = token

    for token in translation_unit.cursor.walk_preorder():
        if (
            token.kind == cindex.CursorKind.BINARY_OPERATOR
            or token.kind == cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR
        ):
            for child in token.get_children():
                if child.kind == cindex.CursorKind.DECL_REF_EXPR:
                    for reference in child.referenced.walk_preorder():
                        if reference.kind == cindex.CursorKind.VAR_DECL:
                            all_var_decls[hash(reference)] = None

    for _, the_used_token in all_var_decls.items():
        if the_used_token:
            violation = checker.extract_violation(
                the_used_token,
                "TIDY_SAMO_MISSING_CONST",
                f"The variable {the_used_token.spelling} could be made const",
            )
            if violation:
                violations.append(violation)

    return violations
