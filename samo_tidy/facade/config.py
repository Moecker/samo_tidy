import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.samo_nested_namespaces_checker as samo_nested_namespaces_checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.checker.samo_unsigned_int_checker as samo_unsigned_int_checker
import samo_tidy.checker.samo_missing_const_checker as samo_missing_const_checker

active_checkers = [
    samo_multiple_classes_checker.translation_unit_based_rule,
    samo_nested_namespaces_checker.translation_unit_based_rule,
    samo_missing_const_checker.translation_unit_based_rule,
    samo_suffix_case_checker.token_based_rule,
    samo_unsigned_int_checker.token_based_rule,
]


def get_checker_registry():
    registry = set(active_checkers)
    return registry
