import unittest

import samo_tidy.checker.samo_nested_namespaces_checker as the_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoMultipleClassesChecker(test_checker_lib.TestCheckerLib):
    def test_positiv(self):
        filename = test_support.create_tempfile(["namespace a { namespace b { } }"])
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            test_support.create_tempfile(["namespace a { namespace b { } }"]),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 1)

    def test_negativ(self):
        violations, diagnostics = self.apply_checker(
            the_checker.translation_unit_based_rule,
            test_support.create_tempfile(["class A", "{", "};"]),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    test_support.default_test_setup()
