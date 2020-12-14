import unittest
import logging
import sys
import os

from clang import cindex
from unittest.mock import patch

import samo_tidy.test.test_utils as test_utils
import samo_tidy.facade.facade as facade
import samo_tidy.core.tu_parser as tu_parser


class TestFacade(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "../../test/data")
        cindex.Config.loaded = False

    def set_arguments(self, arguments):
        sys.argv = [sys.argv[0]]
        sys.argv.extend(arguments)

    def assert_exit_code(self, function, exit_code):
        with self.assertRaises(SystemExit) as context:
            function()
        self.assertEqual(context.exception.code, exit_code)

    def test_missing_arguments(self):
        self.set_arguments([])
        # Raised by arg-parser on missing mandatory fields
        self.assert_exit_code(facade.main, 2)

    def test_default_arguments_missing_db(self):
        self.set_arguments(["--compdb", "/tmp"])
        self.assert_exit_code(facade.main, "Loading of compdb failed")

    def test_default_arguments_valid_but_empty_db(self):
        self.set_arguments(["--compdb", self.test_data_dir])
        self.assert_exit_code(facade.main, 0)

    @patch("platform.system")
    def test_windows_unsupported(self, mock_system):
        mock_system.return_value = "Windows"
        self.set_arguments(["--compdb", "/tmp"])
        self.assert_exit_code(facade.main, "Windows is not supported")

    def test_apply_checkers_for_translation_units(self):
        source_file = test_utils.create_temp_file_for([""])
        tu = tu_parser.create_translation_unit(source_file)
        number_of_successfull_tus = facade.apply_checkers_for_translation_units([tu])
        self.assertEqual(1, number_of_successfull_tus)


if __name__ == "__main__":
    test_utils.default_test_setup()
