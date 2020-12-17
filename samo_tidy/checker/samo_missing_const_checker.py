from clang import cindex

import samo_tidy.checker.checker as checker
import samo_tidy.dump.dump as dump


def translation_unit_based_rule(translation_unit):
    violations = []
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.DECL_REF_EXPR:
            if token.referenced:
                print(
                    f"The token {token.kind} in {dump.pretty_location(token.location)} as definition={token.is_definition()} is used"
                )
                is_used = False
                for reference in token.referenced.walk_preorder():
                    print(
                        f"\tby token {reference.kind} in {dump.pretty_location(reference.location)} as definition={reference.is_definition()}"
                    )

                    if reference.kind == cindex.CursorKind.VAR_DECL:
                        is_used = True
                if not is_used:
                    violation = checker.extract_violation(
                        token,
                        "TIDY_SAMO_MISSING_CONST",
                        f"The variable {token.spelling} could be made const",
                    )
                    if violation:
                        violations.append(violation)
                        break
    return violations
