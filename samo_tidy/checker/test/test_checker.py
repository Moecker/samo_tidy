import unittest

import samo_tidy.checker.checker as checker

import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_utils as test_utils


def get_simple_non_conforming_suffix_source():
    return ["#include <cstdint>", "std::uint8_t F();", "std::uint8_t F()", "{", "std::uint8_t a=0u;", "return a;", "}"]


class TestChecker(test_checker_lib.TestCheckerLib):
    def test_ignored_file_name_positive(self):
        file_name = test_utils.create_temp_file_for(get_simple_non_conforming_suffix_source(), "/tmp/usr/ignore_me.cpp")
        violations, diagnostics = self.apply_random_check(file_name)
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(diagnostics), 0)

    def test_ignored_file_name_negative(self):
        file_name = test_utils.create_temp_file_for(
            get_simple_non_conforming_suffix_source(), "/tmp/do_not_ignore_me.cpp"
        )
        violations, diagnostics = self.apply_random_check(file_name)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].file_name, "do_not_ignore_me.cpp")
        self.assertEqual(violations[0].file_path, "/tmp/do_not_ignore_me.cpp")
        self.assertEqual(len(diagnostics), 0)

    def test_shall_ignore_based_on_file_name(self):
        self.assertTrue(checker.shall_ignore_based_on_file_name("/usr/foo.cpp"))
        self.assertTrue(checker.shall_ignore_based_on_file_name("/tmp/usr/ignore_me.cpp"))
        self.assertFalse(checker.shall_ignore_based_on_file_name("foo.cpp"))

    def test_header_files_get_analyzed(self):
        cpp_file = test_utils.create_temp_file_for(['#include "header.h"', ""], "cpp_file.cpp")
        _ = test_utils.create_temp_file_for(get_simple_non_conforming_suffix_source(), "header.h")
        violations, diagnostics = self.apply_random_check(cpp_file)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].file_name, "header.h")
        self.assertEqual(len(diagnostics), 0)


if __name__ == "__main__":
    test_utils.default_test_setup()
