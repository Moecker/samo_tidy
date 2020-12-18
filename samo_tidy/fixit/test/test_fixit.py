import unittest

import samo_tidy.fixit.fixit as fixit
import samo_tidy.test.test_support as test_support
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
from samo_tidy.checker.violation import Violation


class TestFixit(unittest.TestCase):
    def assert_fix(self, violation, fixed_line):
        with open(violation.file_path) as the_file:
            self.assertEqual(the_file.readlines()[violation.line - 1].strip(), fixed_line)

    def test_fixit_template_for_suffix(self):
        filename = test_support.create_tempfile(["std::uint8_t var = 1u;"])
        violation = Violation("TIDY_SAMO_SUFFIX_CASE", "", filename, 1, 20)

        fixed_lines = fixit.fix_violation(violation, samo_suffix_case_checker.fix)
        self.assertTrue(fixed_lines)
        self.assert_fix(violation, "std::uint8_t var = 1U;")

    def test_fixit_template_for_suffix(self):
        filename = test_support.create_tempfile(["std::uint8_t var = 1u;"])
        violation = Violation("TIDY_SAMO_INVALID_ID", "", filename, 1, 20)

        fixed_lines = fixit.fix_violation(violation, samo_suffix_case_checker.fix)
        self.assertFalse(fixed_lines)
        self.assert_fix(violation, "std::uint8_t var = 1u;")

    def test_fixit_template_for_suffix_multiple(self):
        filename = test_support.create_tempfile(
            ["std::uint8_t my_first_var = 1u;", "std::uint32_t my_second_var = 123u;"]
        )
        violation1 = Violation("TIDY_SAMO_SUFFIX_CASE", "", filename, 1, 29)
        violation2 = Violation("TIDY_SAMO_SUFFIX_CASE", "", filename, 2, 33)
        violations = [violation1, violation2]

        fixit.fix_violations(violations, samo_suffix_case_checker.fix)

        self.assert_fix(violation1, "std::uint8_t my_first_var = 1U;")
        self.assert_fix(violation2, "std::uint32_t my_second_var = 123U;")


if __name__ == "__main__":
    test_support.default_test_setup()
