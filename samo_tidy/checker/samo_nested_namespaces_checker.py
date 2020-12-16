from clang import cindex

import samo_tidy.checker.checker as checker

# Checks for multiple classes in one translation unit
def translation_unit_based_rule(translation_unit):
    violations = []
    namespaces = []

    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.NAMESPACE:
            if token.is_definition:
                namespaces.append(token.spelling)

    if len(namespaces) > 1:
        violation = checker.extract_violation(
            token,
            "TIDY_SAMO_NESTED_NAMESPACE",
            f"Multiple {len(namespaces)} namespaces in one translation unit",
        )
        if violation:
            violations.append(violation)
    return violations
