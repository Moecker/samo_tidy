from unittest.mock import patch
import unittest

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.facade.facade as facade
import samo_tidy.facade.test.test_facade_lib as test_facade_lib
import samo_tidy.test.test_support as test_support


class TestFacade(test_facade_lib.TestFacadeLib):
    def test_missing_arguments(self):
        self.set_arguments([])
        # Raised by arg-parser on missing mandatory fields
        self.assert_exit_code(facade.main, 2)

    def test_default_arguments_missing_db(self):
        self.set_arguments(["--compdb", "/tmp", "--log_level", test_support.get_default_log_level_for_tests()])
        self.assert_exit_code(facade.main, "Loading of compdb failed")

    def test_default_arguments_valid_but_empty_db(self):
        self.set_arguments(
            ["--compdb", self.single_compdb_root, "--log_level", test_support.get_default_log_level_for_tests()]
        )
        self.assert_exit_code(facade.main, 0)

    @patch("platform.system")
    def test_windows_unsupported(self, mock_system):
        mock_system.return_value = "Windows"
        self.set_arguments(["--compdb", "/tmp", "--log_level", test_support.get_default_log_level_for_tests()])
        self.assert_exit_code(facade.main, "Windows is not supported")

    def test_apply_checkers_for_translation_units(self):
        source_file = test_support.create_tempfile([""])
        tu = tu_parser.create_translation_unit(source_file)
        facade.apply_checkers_for_translation_units([tu])
        # TODO Expect no call to the checkers as we have an invalid tu


if __name__ == "__main__":
    test_support.default_test_setup()
