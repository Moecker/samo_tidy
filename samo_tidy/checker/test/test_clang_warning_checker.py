import unittest

from unittest import skip

from samo_tidy.checker.clang_warning_checker import check_for_clang_warnings
from samo_tidy.test.test_utils import default_test_setup, create_temp_file_for
from samo_tidy.core.tu_parser import create_translation_unit


class TestChecker(unittest.TestCase):
    def test_unused_variable(self):
        file_name = create_temp_file_for(["int main()", "{", "int a;", "return 0;", "}"])
        tu = create_translation_unit(file_name)
        violations = check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].id, "TIDY_UNUSED_VARIABLE")
        self.assertEqual(violations[0].message, "unused variable 'a'")

    def test_impl_conversion(self):
        file_name = create_temp_file_for(
            ["#include <cstdint>", "std::uint8_t F();", "uint8_t F()", "{", "int a=1;", "return a;", "}"]
        )
        tu = create_translation_unit(file_name)
        violations = check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].id, "TIDY_IMPLICIT_INT_CONVERSION")
        self.assertEqual(
            violations[0].message,
            "implicit conversion loses integer precision: 'int' to 'uint8_t' (aka 'unsigned char')",
        )

    def test_non_location_warning(self):
        file_name = create_temp_file_for([""])
        tu = create_translation_unit(file_name, args=["clang++"])
        violations = check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    default_test_setup()
