import unittest
import os
import logging

from pprint import pformat
from clang import cindex

import samo_tidy.checker.checker as checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.utils.cindex_dump as cindex_dump


class TestCheckerLib(unittest.TestCase):
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
