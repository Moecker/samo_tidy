import unittest
import clang
import os
import logging
from pprint import pformat

from clang import cindex

from samo_tidy.checker.checker import check_for_ints
from samo_tidy.utils.utils import debug_file_content, setup_clang, get_diag_info


def create_translation_unit(source_file):
    index = cindex.Index.create()
    tu = index.parse(source_file, args=[])
    logging.info(pformat(("diags", [get_diag_info(d) for d in tu.diagnostics])))
    pformat(("diags", [get_diag_info(d) for d in tu.diagnostics]))
    return tu


class TestChecker(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")

    def get_source_file_path(self, file_name):
        source_file = os.path.join(self.test_data_dir, file_name)
        debug_file_content(source_file)
        return source_file

    def check_ints(self, source_file):
        tu = create_translation_unit(source_file)
        violations = check_for_ints(tu)
        return violations

    def test_check_for_ints_id1(self):
        source_file = self.get_source_file_path("source_id1.cpp")
        violations = self.check_ints(source_file)
        self.assertEqual(len(violations), 1)
        self.assertIn("source_id1.cpp", violations[0].file)
        self.assertEqual("TIDY_SUFFIX_CASE", violations[0].id)

    def test_check_for_ints_id2(self):
        source_file = self.get_source_file_path("source_id2.cpp")
        violations = self.check_ints(source_file)
        self.assertEqual(len(violations), 0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    setup_clang()
    unittest.main()