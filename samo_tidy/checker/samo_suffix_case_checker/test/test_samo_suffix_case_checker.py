import os
import unittest

from samo_tidy.checker.violation import Violation
import samo_tidy.checker.samo_suffix_case_checker.samo_suffix_case_checker as the_checker
import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.fixit.fixit as fixit
import samo_tidy.test.test_support as test_support


class TestSamoSuffixCaseChecker(test_checker_lib.TestCheckerLib):
    def setUp(self):
        super().setUp()
        self.checker_test_files = os.path.join(os.path.dirname(__file__), "data")

    def test_check_for_ints_id1(self):
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule, self.get_source_file_path("source_id1.cpp")
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(len(diagnostics), 1)
        self.assertIn("source_id1.cpp", violations[0].file_path)
        self.assertEqual("TIDY_SAMO_SUFFIX_CASE", violations[0].id)
        self.assertEqual("-Wunused-variable", diagnostics[0].option)

    def test_check_for_ints_id2(self):
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule, self.get_source_file_path("source_id2.cpp")
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)

    def test_check_for_ints_id3(self):
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule, self.get_source_file_path("source_id3.cpp")
        )
        self.assertEqual(len(diagnostics), 1)
        self.assertIn("expected ';'", diagnostics[0].spelling)

    def test_check_for_ints_id4(self):
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule,
            self.get_source_file_path("source_id4.cpp"),
            [f"-I{self.test_data_dir}"],
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)

    def test_temp_file_int(self):
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule,
            test_support.create_tempfile(["int F();", "int F()", "{", "return 0;", "}"]),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)

    def test_temp_file_uint(self):
        file_name = test_support.create_tempfile(
            ["#include <cstdint>", "std::uint8_t F();", "std::uint8_t F()", "{", "return 0u;", "}"]
        )
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule,
            file_name,
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 1)
        self.assertIn(file_name, violations[0].file_path)
        self.assertEqual("TIDY_SAMO_SUFFIX_CASE", violations[0].id)

    def test_temp_file_uint_conversion(self):
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule,
            test_support.create_tempfile(
                ["#include <cstdint>", "int main()", "{", "int a = 12;", "std::uint8_t b = a;", "}"]
            ),
        )
        self.assertEqual(len(diagnostics), 2)
        self.assertEqual("-Wimplicit-int-conversion", diagnostics[0].option)
        self.assertEqual("-Wunused-variable", diagnostics[1].option)
        self.assertEqual(len(violations), 0)

    def test_temp_file_uint_conversion_fine(self):
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule,
            test_support.create_tempfile(
                ["#include <cstdint>", "int main()", "{", "std::uint8_t b = 123;", "return b;" "}"]
            ),
        )
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)

    def test_validate(self):
        filename = os.path.join(self.checker_test_files, "samo_suffix_case_checker.cpp")
        violations, diagnostics = self.apply_checker(
            the_checker.token_based_rule,
            filename,
        )
        self.assertEqual(len(diagnostics), 0)
        self.validate(filename, violations)

    def test_fixit(self):
        lines = ["std::uint8_t F()", "{", "return 0u;", "}"]
        line_index = 3
        violation = Violation(
            "TIDY_SAMO_SUFFIX_CASE",
            "message",
            "filepath",
            line_index,
            8,
        )
        new_lines = fixit.apply_fix_per_line(lines, violation, the_checker.fix_rule)
        self.assertEqual(new_lines[line_index - 1], "return 0U;")


if __name__ == "__main__":
    test_support.default_test_setup()
