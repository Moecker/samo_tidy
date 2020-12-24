from clang import cindex
from pprint import pformat
import logging
import os
import unittest

import samo_tidy.checker.checker as checker
import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.dump as dump
import samo_tidy.utils.utils as utils


class TestCheckerLib(unittest.TestCase):
    def apply_checker(self, rule, source_file, args=[]):
        translation_unit = tu_parser.create_translation_unit(source_file, args)
        self.assertTrue(translation_unit)
        violations = checker.apply_checker(translation_unit, rule)
        return violations, translation_unit.diagnostics

    def dump(self, source_file, args=[]):
        translation_unit = tu_parser.create_translation_unit(source_file, args)
        logging.debug(pformat(("nodes", dump.get_info(translation_unit.cursor))))

    def get_number_of_expected_violations(self, file_name):
        number_of_expected_violations = 0
        with open(file_name) as the_file:
            lines = the_file.readlines()
            for line in lines:
                if not utils.is_commented_line(line) and "TIDY_SAMO" in line:
                    number_of_expected_violations += 1
        return number_of_expected_violations

    def get_source_file_path(self, file_name):
        source_file = os.path.join(self.test_data_dir, file_name)
        return source_file

    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "../../test/data/cpp_files")
        self.checker_test_files = os.path.join(os.path.dirname(__file__), "data")

    def validate(self, file_name, violations):
        number_of_expected_violations = 0
        with open(file_name) as the_file:
            lines = the_file.readlines()
            for line in lines:
                if not utils.is_commented_line(line) and "TIDY_SAMO" in line:
                    number_of_expected_violations += 1
            self.assertEqual(number_of_expected_violations, len(violations))
            for violation in violations:
                violated_line = lines[violation.line - 1].strip()
                self.assertIn(violation.id, violated_line)
