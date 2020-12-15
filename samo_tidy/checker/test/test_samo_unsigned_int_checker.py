import unittest

import samo_tidy.checker.samo_unsigned_int_checker as samo_unsigned_int_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


class TestSamoUnsignedIntChecker(test_checker_lib.TestCheckerLib):
    def test_check_for_unsigned_ints(self):
        violations, diagnostics = self.apply_checker(
            samo_unsigned_int_checker.token_based_rule,
            test_support.create_tempfile(
                [
                    "int main()",
                    "{",
                    "return 1u;",
                    "}",
                ]
            ),
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(len(diagnostics), 0)


if __name__ == "__main__":
    test_support.default_test_setup()
