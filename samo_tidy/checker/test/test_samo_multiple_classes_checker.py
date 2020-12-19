import os
import unittest

import samo_tidy.checker.samo_multiple_classes_checker as the_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoMultipleClassesChecker(test_checker_lib.TestCheckerLib):
    def test_check_for_multiple_classes_positiv(self):
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            test_support.create_tempfile(["class A", "{", "};", "class B", "{", "};"]),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 2)
        self.assertEqual(violations[0].id, "TIDY_SAMO_MULTIPLE_CLASSES")
        self.assertIn("Multiple of 2 classes", violations[0].message)
        self.assertIn("'A'", violations[0].message)
        self.assertIn("'B'", violations[1].message)

    def test_check_for_multiple_classes_only_usage(self):
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            test_support.create_tempfile(
                ["class A", "{", "public:", "int b;", "};", "int main()", "{", "A a;", "return a.b;", "}"]
            ),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)

    def test_check_for_multiple_classes_negativ(self):
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            test_support.create_tempfile(["class A", "{", "};"]),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)

    def test_validate(self):
        filename = os.path.join(self.checker_test_files, "samo_multiple_classes_checker.cpp")
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.validate(filename, violations)


if __name__ == "__main__":
    test_support.default_test_setup()
