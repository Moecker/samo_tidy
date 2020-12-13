import unittest
import os
import logging

from pprint import pformat
from clang import cindex

import samo_tidy.checker.checker as checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.utils.cindex_dump as cindex_dump

import samo_tidy.test.test_utils as test_utils


class TestChecker(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "../../test/data")

    def apply_random_check(self, source_file):
        tu = tu_parser.create_translation_unit(source_file)
        violations = checker.apply_checker(tu, samo_suffix_case_checker.rule)
        return violations

    def get_source_file_path(self, file_name):
        source_file = os.path.join(self.test_data_dir, file_name)
        return source_file

    def dump(self, source_file, args=[]):
        tu = tu_parser.create_translation_unit(source_file, args)
        logging.debug(pformat(("nodes", cindex_dump.get_info(tu.cursor))))

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
