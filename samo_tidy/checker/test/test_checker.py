import unittest

import samo_tidy.checker.checker as checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker

import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_support as test_support


def get_simple_non_conforming_suffix_source():
    return ["#include <cstdint>", "std::uint8_t F();", "std::uint8_t F()", "{", "std::uint8_t a=0u;", "return a;", "}"]


class TestChecker(test_checker_lib.TestCheckerLib):
    def test_ignored_file_name_positive(self):
        violations, diagnostics = self.apply_checker(
            samo_suffix_case_checker.token_based_rule,
            test_support.create_tempfile(
                get_simple_non_conforming_suffix_source(),
                "/tmp/usr/ignore_me.cpp",
            ),
        )
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(diagnostics), 0)

    def test_ignored_file_name_negative(self):
        violations, diagnostics = self.apply_checker(
            samo_suffix_case_checker.token_based_rule,
            test_support.create_tempfile(get_simple_non_conforming_suffix_source(), "/tmp/do_not_ignore_me.cpp"),
        )
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].file_name, "do_not_ignore_me.cpp")
        self.assertEqual(violations[0].file_path, "/tmp/do_not_ignore_me.cpp")
        self.assertEqual(len(diagnostics), 0)

    def test_header_files_get_analyzed(self):
        cpp_file = test_support.create_tempfile(['#include "header.h"', ""], "cpp_file.cpp")
        # Just so it is available
        _ = test_support.create_tempfile(get_simple_non_conforming_suffix_source(), "header.h")
        violations, diagnostics = self.apply_checker(samo_suffix_case_checker.token_based_rule, cpp_file)
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].file_name, "header.h")
        self.assertEqual(len(diagnostics), 0)


if __name__ == "__main__":
    test_support.default_test_setup()
