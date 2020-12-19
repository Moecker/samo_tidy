import os
import unittest

import samo_tidy.checker.samo_nested_namespaces_checker as the_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoMultipleClassesChecker(test_checker_lib.TestCheckerLib):
    def test_positiv(self):
        filename = test_support.create_tempfile(["namespace a {", "namespace b {", "}", "}"])
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].id, "TIDY_SAMO_NESTED_NAMESPACE")
        self.assertEqual(violations[0].line, 2)
        self.assertEqual(violations[0].column, 11)

    def test_three_levels(self):
        filename = test_support.create_tempfile(["namespace a { namespace b { namespace c { } } }"])
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 2)
        self.assertIn("2 nested", violations[0].message)
        self.assertIn("3 nested", violations[1].message)

    def test_negativ(self):
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            test_support.create_tempfile(["namespace a {} namespace b {}"]),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)

    def test_validate(self):
        filename = os.path.join(self.checker_test_files, "samo_nested_namespaces_checker.cpp")
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.validate(filename, violations)


if __name__ == "__main__":
    test_support.default_test_setup()
