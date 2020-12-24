import os

import samo_tidy.checker.samo_class_name_checker.samo_class_name_checker as samo_class_name_checker
import samo_tidy.checker.samo_missing_const_checker.samo_missing_const_checker as samo_missing_const_checker
import samo_tidy.checker.samo_multiple_classes_checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.samo_nested_namespaces_checker.samo_nested_namespaces_checker as samo_nested_namespaces_checker
import samo_tidy.checker.samo_suffix_case_checker.samo_suffix_case_checker as samo_suffix_case_checker


ALL_CHECKERS = [
    samo_class_name_checker.translation_unit_based_rule,
    samo_missing_const_checker.translation_unit_based_rule,
    samo_multiple_classes_checker.translation_unit_based_rule,
    samo_nested_namespaces_checker.translation_unit_based_rule,
    samo_suffix_case_checker.token_based_rule,
]

ALL_FIXITS = [
    samo_missing_const_checker.fix_rule,
    samo_suffix_case_checker.fix_rule,
]


class Config:
    def __init__(self, active_checkers, compdb, files, log_level, log_file, workers, fix):
        self._compdb = compdb
        self.active_checkers = active_checkers
        self.files = files
        self.fix = fix
        self.log_file = log_file
        self.log_level = log_level
        self.workers = workers

    @property
    def compdb(self):
        return self._compdb

    @compdb.setter
    def compdb(self, value):
        self._compdb = value

    def present(self):
        return {
            "Active checkers": [checker.__module__ for checker in self.active_checkers],
            "Apply fixes": self.fix,
            "Compdb path": os.path.join(self.compdb, "compile_commands.json"),
            "File filter": self.files,
            "Log file": self.log_file,
            "Log level": self.log_level,
            "Number of workers": self.workers,
        }
