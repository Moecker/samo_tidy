import unittest
import os
import logging

from clang import cindex

import samo_tidy.checker.checker as checker
import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.core.tu_parser as tu_parser

import samo_tidy.test.test_utils as test_utils
import samo_tidy.checker.test.test_checker_lib as test_checker_lib


class TestSamoMultipleClassesChecker(test_checker_lib.TestCheckerLib):
    def apply_checker(self, source_file, args=[]):
        tu = tu_parser.create_translation_unit(source_file, args)
        violations = checker.apply_checker(tu, samo_multiple_classes_checker.rule)
        return violations, tu.diagnostics

    def test_check_for_ints_id1(self):
        file_name = test_utils.create_temp_file_for(["int F();", "int F()", "{", "return 0;", "}"])
        violations, diagnostics = self.apply_checker(file_name)
        self.assertEqual(len(violations), 1)
        self.assertEqual(len(diagnostics), 0)


if __name__ == "__main__":
    test_utils.default_test_setup()
