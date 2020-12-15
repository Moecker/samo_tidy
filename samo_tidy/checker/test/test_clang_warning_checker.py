import unittest

import samo_tidy.checker.clang_warning_checker as clang_warning_checker
import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.test.test_support as test_support


class TestChecker(unittest.TestCase):
    def test_unused_variable(self):
        tu = tu_parser.create_translation_unit(
            test_support.create_tempfile(["int main()", "{", "int a;", "return 0;", "}"])
        )
        violations = clang_warning_checker.check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].id, "TIDY_CLANG_UNUSED_VARIABLE")
        self.assertEqual(violations[0].message, "unused variable 'a'")

    def test_impl_conversion(self):
        tu = tu_parser.create_translation_unit(
            test_support.create_tempfile(
                ["#include <cstdint>", "std::uint8_t F();", "uint8_t F()", "{", "int a=1;", "return a;", "}"]
            )
        )
        violations = clang_warning_checker.check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].id, "TIDY_CLANG_IMPLICIT_INT_CONVERSION")
        self.assertEqual(
            violations[0].message,
            "implicit conversion loses integer precision: 'int' to 'uint8_t' (aka 'unsigned char')",
        )

    def test_non_location_warning(self):
        tu = tu_parser.create_translation_unit(test_support.create_tempfile([""]), args=["clang++"])
        violations = clang_warning_checker.check_for_clang_warnings(tu)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    test_support.default_test_setup()
