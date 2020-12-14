import unittest

import samo_tidy.checker.checker as checker

import samo_tidy.checker.test.test_checker_lib as test_checker_lib
import samo_tidy.test.test_utils as test_utils


class TestChecker(test_checker_lib.TestCheckerLib):
    def test_ignored_file_name(self):
        file_name = test_utils.create_temp_file_for(
            ["#include <cstdint>", "std::uint8_t a=0u;"], "/tmp/usr/ignore_me.cpp"
        )
        violations = self.apply_random_check(file_name)
        self.assertEqual(len(violations), 0)
        file_name = test_utils.create_temp_file_for(
            ["#include <cstdint>", "std::uint8_t a=0u;"], "/tmp/do_not_ignore_me.cpp"
        )
        violations = self.apply_random_check(file_name)
        self.assertEqual(len(violations), 1)

    def test_shall_ignore_based_on_file_name(self):
        self.assertTrue(checker.shall_ignore_based_on_file_name("/usr/foo.cpp"))
        self.assertTrue(checker.shall_ignore_based_on_file_name("/tmp/usr/ignore_me.cpp"))
        self.assertFalse(checker.shall_ignore_based_on_file_name("foo.cpp"))


if __name__ == "__main__":
    test_utils.default_test_setup()
