import unittest
import clang
import os
import logging
from clang import cindex

from samo_tidy.checker.checker import check_for_ints
from samo_tidy.utils.utils import debug_file_content, setup_clang


def create_translation_unit(source_file):
    index = cindex.Index.create()
    return index.parse(source_file, args=[])


class TestChecker(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

    def test_check_for_ints(self):
        test_data_dir = os.path.join(os.path.dirname(__file__), "data")
        source_file = os.path.join(test_data_dir, "source_id1.cpp")
        debug_file_content(source_file)
        tu = create_translation_unit(source_file)
        check_for_ints(tu)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    setup_clang()
    unittest.main()