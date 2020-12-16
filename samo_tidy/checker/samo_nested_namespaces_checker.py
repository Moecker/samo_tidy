from clang import cindex
from collections import defaultdict

import samo_tidy.checker.checker as checker

# Checks for nested namespaces in one translation unit
def translation_unit_based_rule(translation_unit):
    violations = []
    nested_namespaces = defaultdict(list)

    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.NAMESPACE:
            if token.is_definition:
                if token.location.file.name == translation_unit.spelling:
                    # TODO Rather use a child-token traversal
                    if token.get_usr().count("@N") > 1:
                        nested_namespaces[token.spelling].append(token)

    for _, nestings_per_namespace in nested_namespaces.items():
        for nesting_per_namespace in nestings_per_namespace:
            violation = checker.extract_violation(
                nesting_per_namespace,
                "TIDY_SAMO_NESTED_NAMESPACE",
                f"Multiple of {len(nested_namespaces.items())} namespaces in one translation unit",
            )
            if violation:
                violations.append(violation)
    return violations
