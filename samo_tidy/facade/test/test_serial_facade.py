from unittest.mock import patch
import unittest

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.facade.serial_facade as serial_facade
import samo_tidy.facade.facade_lib as facade_lib
import samo_tidy.facade.test.test_facade_lib as test_facade_lib
import samo_tidy.test.test_support as test_support
import samo_tidy.core.summary as summary


class TestFacade(test_facade_lib.TestFacadeLib):
    def test_missing_arguments(self):
        test_support.set_arguments([])
        # Raised by arg-parser on missing mandatory fields
        self.assert_exit_code(serial_facade.main, 2)

    def test_default_arguments_missing_db(self):
        test_support.set_arguments(["--compdb", "/tmp", "--log_level", test_support.get_default_log_level_for_tests()])
        self.assert_exit_code(serial_facade.main, "ERROR: Loading of compdb failed")

    def test_default_arguments_valid_but_empty_db(self):
        test_support.set_arguments(
            ["--compdb", self.single_compdb_root, "--log_level", test_support.get_default_log_level_for_tests()]
        )
        self.assert_exit_code(serial_facade.main, 0)

    @patch("platform.system")
    def test_windows_unsupported(self, mock_system):
        mock_system.return_value = "Windows"
        test_support.set_arguments(["--compdb", "/tmp", "--log_level", test_support.get_default_log_level_for_tests()])
        self.assert_exit_code(serial_facade.main, "ERROR: Windows is not supported")

    def test_apply_checkers_for_translation_units(self):
        source_file = test_support.create_tempfile([""])
        tu = tu_parser.create_translation_unit(source_file)
        all_violations = facade_lib.apply_checkers_for_translation_units([tu], self.the_config)
        self.assertEqual([], all_violations)

    @patch("samo_tidy.facade.facade_lib.apply_checkers_for_commands")
    @patch("samo_tidy.core.compdb_parser.parse_compdb")
    def test_run_serial(self, mock_parse_compdb, mock_apply_checkers_for_commands):
        mock_parse_compdb.return_value = []
        serial_facade.run_serial(self.the_config, None)
        mock_apply_checkers_for_commands.assert_called_with(mock_parse_compdb.return_value, self.the_config)


if __name__ == "__main__":
    test_support.default_test_setup()
