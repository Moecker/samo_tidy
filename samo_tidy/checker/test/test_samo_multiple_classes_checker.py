import unittest

import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoMultipleClassesChecker(test_checker_lib.TestCheckerLib):
    def test_check_for_multiple_classes_positiv(self):
        violations, diagnostics = self.apply_checker(
            samo_multiple_classes_checker.translation_unit_based_rule,
            test_support.create_tempfile(["class A", "{", "};", "class B", "{", "};"]),
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(len(diagnostics), 0)

    def test_check_for_multiple_classes_negativ(self):
        violations, diagnostics = self.apply_checker(
            samo_multiple_classes_checker.translation_unit_based_rule,
            test_support.create_tempfile(["class A", "{", "};"]),
        )
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(diagnostics), 0)


if __name__ == "__main__":
    test_support.default_test_setup()
