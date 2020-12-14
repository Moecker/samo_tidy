import unittest

import samo_tidy.checker.clang_warning_checker as clang_warning_checker
import samo_tidy.core.tu_parser as tu_parser

import samo_tidy.test.test_utils as test_utils


class TestChecker(unittest.TestCase):
    def test_unused_variable(self):
        file_name = test_utils.create_temp_file_for(["int main()", "{", "int a;", "return 0;", "}"])
        tu = tu_parser.create_translation_unit(file_name)
        violations = clang_warning_checker.check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].id, "TIDY_CLANG_UNUSED_VARIABLE")
        self.assertEqual(violations[0].message, "unused variable 'a'")

    def test_impl_conversion(self):
        file_name = test_utils.create_temp_file_for(
            ["#include <cstdint>", "std::uint8_t F();", "uint8_t F()", "{", "int a=1;", "return a;", "}"]
        )
        tu = tu_parser.create_translation_unit(file_name)
        violations = clang_warning_checker.check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].id, "TIDY_CLANG_IMPLICIT_INT_CONVERSION")
        self.assertEqual(
            violations[0].message,
            "implicit conversion loses integer precision: 'int' to 'uint8_t' (aka 'unsigned char')",
        )

    def test_non_location_warning(self):
        file_name = test_utils.create_temp_file_for([""])
        tu = tu_parser.create_translation_unit(file_name, args=["clang++"])
        violations = clang_warning_checker.check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    test_utils.default_test_setup()
