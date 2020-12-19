import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.samo_nested_namespaces_checker as samo_nested_namespaces_checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.checker.samo_unsigned_int_checker as samo_unsigned_int_checker
import samo_tidy.checker.samo_missing_const_checker as samo_missing_const_checker

ALL_CHECKERS = [
    samo_missing_const_checker.translation_unit_based_rule,
    samo_multiple_classes_checker.translation_unit_based_rule,
    samo_nested_namespaces_checker.translation_unit_based_rule,
    samo_suffix_case_checker.token_based_rule,
    samo_unsigned_int_checker.token_based_rule,
]


class Config:
    def __init__(self, active_checkers, compdb, files, log_level, workers, fix):
        self.active_checkers = active_checkers
        self._compdb = compdb
        self.files = files
        self.log_level = log_level
        self.workers = workers
        self.fix = fix

    @property
    def compdb(self):
        return self._compdb

    @compdb.setter
    def compdb(self, value):
        self._compdb = value
