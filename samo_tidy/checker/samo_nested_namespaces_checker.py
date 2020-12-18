from clang import cindex
from collections import defaultdict

import samo_tidy.checker.checker as checker

MAX_DEPTH_ALLOWED = 1

# Checks for nested namespaces in one translation unit
def translation_unit_based_rule(translation_unit):
    violations = []
    nested_namespaces = defaultdict(list)

    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.NAMESPACE:
            if token.is_definition:
                if token.location.file.name == translation_unit.spelling:
                    # TODO Rather use a child-token traversal
                    number_of_nestings = token.get_usr().count("@N")
                    if number_of_nestings > MAX_DEPTH_ALLOWED:
                        nested_namespaces[token.spelling].append((token, number_of_nestings))

    for _, nestings_per_namespace in nested_namespaces.items():
        for nesting_per_namespace, number_of_nestings in nestings_per_namespace:
            violation = checker.extract_violation(
                nesting_per_namespace,
                "TIDY_SAMO_NESTED_NAMESPACE",
                f"Multiple of {number_of_nestings} nested namespace(s) in one translation unit",
            )
            if violation:
                violations.append(violation)
    return violations
