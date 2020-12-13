import unittest
import logging
import sys
import os

from unittest.mock import patch
from unittest import skip

import samo_tidy.test.test_utils as test_utils
import samo_tidy.facade.facade as facade


class TestFacade(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "../../test/data")

    def set_arguments(self, arguments):
        sys.argv = [sys.argv[0]]
        sys.argv.extend(arguments)

    def assert_exit_code(self, function, exit_code):
        with self.assertRaises(SystemExit) as context:
            function()
        self.assertEqual(context.exception.code, exit_code)

    def test_missing_arguments(self):
        self.set_arguments([])
        self.assert_exit_code(facade.main, 2)  # Raised by arg-parser on missing mandatory fields

    def test_default_arguments_missing_db(self):
        self.set_arguments(["--compdb", "/tmp"])
        self.assert_exit_code(facade.main, "Loading of compdb failed")

    @skip("Does not work as a 'missing clang path' error occurs when calling it twice")
    def test_default_arguments_valid_but_empty_db(self):
        self.set_arguments(["--compdb", self.test_data_dir])
        self.assert_exit_code(facade.main, 0)

    @patch("platform.system")
    def test_windows_unsupported(self, mock_system):
        mock_system.return_value = "Windows"
        self.set_arguments(["--compdb", "/tmp"])
        self.assert_exit_code(facade.main, "Windows is not supported")


if __name__ == "__main__":
    test_utils.default_test_setup()
