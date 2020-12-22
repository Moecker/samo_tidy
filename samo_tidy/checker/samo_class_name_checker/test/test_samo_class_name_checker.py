import os
import unittest

import samo_tidy.checker.samo_class_name_checker.samo_class_name_checker as the_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoClassFileNameChecker(test_checker_lib.TestCheckerLib):
    def setUp(self):
        super().setUp()
        self.checker_test_files = os.path.join(os.path.dirname(__file__), "data")

    def test_validate_translation_unit_based(self):
        filename = os.path.join(self.checker_test_files, "samo_class_name_checker.cpp")
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.validate(filename, violations)


if __name__ == "__main__":
    test_support.default_test_setup()
