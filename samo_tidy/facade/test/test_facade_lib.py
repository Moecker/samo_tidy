from clang import cindex
from unittest.mock import patch
import logging
import os
import sys
import unittest

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.facade.facade as facade
import samo_tidy.test.test_support as test_support


class TestFacadeLib(unittest.TestCase):
    def setUp(self):
        test_data_root = os.path.join(os.path.dirname(__file__), "../../test/data")
        self.single_compdb_root = os.path.join(test_data_root, "single_file_compdb")
        self.multiple_compdb_root = os.path.join(test_data_root, "multiple_files_compdb")

    def assert_exit_code(self, function, exit_code):
        with self.assertRaises(SystemExit) as context:
            function()
        self.assertEqual(context.exception.code, exit_code)


if __name__ == "__main__":
    test_support.default_test_setup()
