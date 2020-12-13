import unittest
import os
import logging

from clang import cindex

import samo_tidy.checker.checker as checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.core.tu_parser as tu_parser

import samo_tidy.test.test_utils as test_utils
import samo_tidy.checker.test.test_checker as test_checker


class TestSamoSuffixCaseChecker(test_checker.TestChecker):
    def apply_samo_suffix_case_checker(self, source_file, args=[]):
        tu = tu_parser.create_translation_unit(source_file, args)
        violations = checker.apply_checker(tu, samo_suffix_case_checker.rule)
        return violations, tu.diagnostics

    def test_check_for_ints_id1(self):
        source_file = self.get_source_file_path("source_id1.cpp")
        violations, diagnostics = self.apply_samo_suffix_case_checker(source_file)
        self.assertEqual(len(violations), 1)
        self.assertEqual(len(diagnostics), 1)
        self.assertIn("source_id1.cpp", violations[0].file_path)
        self.assertEqual("TIDY_SAMO_SUFFIX_CASE", violations[0].id)
        self.assertEqual("-Wunused-variable", diagnostics[0].option)

    def test_check_for_ints_id2(self):
        source_file = self.get_source_file_path("source_id2.cpp")
        violations, diagnostics = self.apply_samo_suffix_case_checker(source_file)
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(diagnostics), 0)

    def test_check_for_ints_id3(self):
        source_file = self.get_source_file_path("source_id3.cpp")
        tu = tu_parser.create_translation_unit(source_file)
        self.assertEqual(len(tu.diagnostics), 1)
        self.assertIn("expected ';'", tu.diagnostics[0].spelling)

    def test_check_for_ints_id4(self):
        source_file = self.get_source_file_path("source_id4.cpp")
        violations, diagnostics = self.apply_samo_suffix_case_checker(source_file, [f"-I{self.test_data_dir}"])
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(diagnostics), 0)

    def test_temp_file_int(self):
        file_name = test_utils.create_temp_file_for(["int F();", "int F()", "{", "return 0;", "}"])
        violations, diagnostics = self.apply_samo_suffix_case_checker(file_name)
        self.assertEqual(len(violations), 0)

    def test_temp_file_uint(self):
        file_name = test_utils.create_temp_file_for(
            ["#include <cstdint>", "std::uint8_t F();", "std::uint8_t F()", "{", "return 0u;", "}"]
        )
        violations, diagnostics = self.apply_samo_suffix_case_checker(file_name)
        self.assertEqual(len(violations), 1)
        self.assertIn(file_name, violations[0].file_path)
        self.assertEqual("TIDY_SAMO_SUFFIX_CASE", violations[0].id)

    def test_temp_file_uint_conversion(self):
        file_name = test_utils.create_temp_file_for(
            ["#include <cstdint>", "int main()", "{", "int a = 12;", "std::uint8_t b = a;", "}"]
        )
        violations, diagnostics = self.apply_samo_suffix_case_checker(file_name)
        self.assertEqual(len(diagnostics), 2)
        self.assertEqual("-Wimplicit-int-conversion", diagnostics[0].option)
        self.assertEqual("-Wunused-variable", diagnostics[1].option)
        self.assertEqual(len(violations), 0)

    def test_temp_file_uint_conversion_fine(self):
        file_name = test_utils.create_temp_file_for(
            ["#include <cstdint>", "int main()", "{", "std::uint8_t b = 123;", "return b;" "}"]
        )
        violations, diagnostics = self.apply_samo_suffix_case_checker(file_name)
        self.assertEqual(len(diagnostics), 0)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    test_utils.default_test_setup()
