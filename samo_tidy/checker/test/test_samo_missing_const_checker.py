import unittest
import os

import samo_tidy.checker.samo_missing_const_checker as the_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoMissingConstChecker(test_checker_lib.TestCheckerLib):
    def test_validate(self):
        filename = os.path.join(self.checker_test_files, "samo_missing_const_checker.cpp")
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.validate(filename, violations)


if __name__ == "__main__":
    test_support.default_test_setup()
