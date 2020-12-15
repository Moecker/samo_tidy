import unittest
import logging
import sys
from clang import cindex
from unittest.mock import patch
import os

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.facade.facade as facade
import samo_tidy.test.test_support as test_support


class TestFacadeLib(unittest.TestCase):
    def setUp(self):
        self.single_compdb_root = os.path.join(os.path.dirname(__file__), "../../test/data")
        self.multiple_compdb_root = os.path.join(self.single_compdb_root, "multiple_files_compdb")

    def set_arguments(self, arguments):
        sys.argv = [sys.argv[0]]
        sys.argv.extend(arguments)

    def assert_exit_code(self, function, exit_code):
        with self.assertRaises(SystemExit) as context:
            function()
        self.assertEqual(context.exception.code, exit_code)


if __name__ == "__main__":
    test_support.default_test_setup()
