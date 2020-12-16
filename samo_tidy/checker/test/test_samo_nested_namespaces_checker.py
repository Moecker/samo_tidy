import unittest
import os

import samo_tidy.checker.samo_nested_namespaces_checker as the_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoMultipleClassesChecker(test_checker_lib.TestCheckerLib):
    def test_positiv(self):
        filename = test_support.create_tempfile(["namespace a { namespace b { } }"])
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 1)

    def test_validate(self):
        filename = os.path.join(self.checker_test_files, "samo_nested_namespaces_checker.cpp")
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 1)
        self.validate(filename, violations)


if __name__ == "__main__":
    test_support.default_test_setup()
