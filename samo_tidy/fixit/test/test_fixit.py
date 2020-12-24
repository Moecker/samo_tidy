import unittest

from samo_tidy.checker.violation import Violation
import samo_tidy.checker.samo_missing_const_checker.samo_missing_const_checker as samo_missing_const_checker
import samo_tidy.checker.samo_suffix_case_checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.fixit.fixit as fixit
import samo_tidy.fixit.test.sample_fix_function as sample_fix_function
import samo_tidy.test.test_support as test_support


class TestFixit(unittest.TestCase):
    def assert_fix(self, violation, fixed_line):
        with open(violation.file_path) as the_file:
            the_lines = the_file.readlines()
            desired_line_number = violation.line - 1
            self.assertGreater(len(the_lines), desired_line_number)
            self.assertEqual(the_lines[violation.line - 1].strip(), fixed_line)

    def test_fix_violation_per_line(self):
        filename = test_support.create_tempfile(["std::uint8_t var = 1u;"])
        violation = Violation("TIDY_DUMMY", "", filename, 1, 0)

        fixit.fix_violation_per_line(violation, sample_fix_function.fix_function)
        self.assert_fix(violation, "Deleted Line")

    def test_fix_violation_per_line_for_missing_const(self):
        filename = test_support.create_tempfile(["int var = 0;"])
        violation = Violation("TIDY_SAMO_MISSING_CONST", "", filename, 1, 5)

        fixit.fix_violation_per_line(violation, samo_missing_const_checker.fix_rule)
        self.assert_fix(violation, "int const var = 0;")

    def test_fixit_template_for_suffix(self):
        filename = test_support.create_tempfile(["std::uint8_t var = 1u;"])
        violation = Violation("TIDY_SAMO_SUFFIX_CASE", "", filename, 1, 20)

        fixed_lines = fixit.fix_violation_per_line(violation, samo_suffix_case_checker.fix_rule)
        self.assertTrue(fixed_lines)
        self.assert_fix(violation, "std::uint8_t var = 1U;")

    def test_fixit_template_for_suffix_invalid(self):
        filename = test_support.create_tempfile(["std::uint8_t var = 1u;"])
        violation = Violation("TIDY_SAMO_INVALID_ID", "", filename, 1, 20)

        fixed_lines = fixit.fix_violation_per_line(violation, samo_suffix_case_checker.fix_rule)
        self.assertFalse(fixed_lines)
        self.assert_fix(violation, "std::uint8_t var = 1u;")

    def test_fixit_template_for_suffix_multiple(self):
        filename = test_support.create_tempfile(
            ["std::uint8_t my_first_var = 1u;", "std::uint32_t my_second_var = 123u;"]
        )
        violation1 = Violation("TIDY_SAMO_SUFFIX_CASE", "", filename, 1, 29)
        violation2 = Violation("TIDY_SAMO_SUFFIX_CASE", "", filename, 2, 33)
        violations = [violation1, violation2]

        fixit.fix_violations_per_line(violations, samo_suffix_case_checker.fix_rule)

        self.assert_fix(violation1, "std::uint8_t my_first_var = 1U;")
        self.assert_fix(violation2, "std::uint32_t my_second_var = 123U;")


if __name__ == "__main__":
    test_support.default_test_setup()
