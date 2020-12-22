from clang import cindex
from collections import defaultdict

import samo_tidy.checker.checker as checker

ID = "TIDY_SAMO_NESTED_NAMESPACE"
MAX_DEPTH_ALLOWED = 1


def translation_unit_based_rule(translation_unit):
    """Checks for nested namespaces in one translation unit"""
    violations = []
    nested_namespaces = defaultdict(list)

    # Set up a list of nested namspaces
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.NAMESPACE:
            if token.is_definition():
                if token.location.file.name == translation_unit.spelling:
                    # TODO Consider use a child-token traversal
                    # The decision about the nesting level of namespace can
                    # be derived from the clang naming count of a special token
                    number_of_nestings = token.get_usr().count("@N")
                    if number_of_nestings > MAX_DEPTH_ALLOWED:
                        nested_namespaces[token.spelling].append((token, number_of_nestings))

    # Create violations based on nested namespaces found
    for _, nestings_per_namespace in nested_namespaces.items():
        for nesting_per_namespace, number_of_nestings in nestings_per_namespace:
            violation = checker.extract_violation(
                nesting_per_namespace,
                ID,
                f"Multiple of {number_of_nestings} nested namespace(s) in one translation unit",
            )
            if violation:
                violations.append(violation)
    return violations
