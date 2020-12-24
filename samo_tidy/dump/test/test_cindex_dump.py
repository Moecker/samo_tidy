import os
import sys
import unittest

import samo_tidy.dump.cindex_dump as cindex_dump
import samo_tidy.test.test_support as test_support


class TestCindexDump(unittest.TestCase):
    def assert_exit_code(self, function, exit_code):
        with self.assertRaises(SystemExit) as context:
            function()
        if type(exit_code) == str:
            self.assertIn(exit_code, context.exception.code)
        else:
            self.assertEqual(exit_code, context.exception.code)

    def setUp(self):
        self.test_data_root = os.path.join(os.path.dirname(__file__), "../../test/data")
        self.existing_file = os.path.join(self.test_data_root, "cpp_files", "source_id1.cpp")
        self.existing_compdb = os.path.join(self.test_data_root, "cpp_files_compdb")

    def test_file_and_compdb(self):
        test_support.set_arguments(["--file", self.existing_file, "--compdb", ""])
        self.assert_exit_code(cindex_dump.main, 0)
        test_support.set_arguments(["--file", self.existing_file, "--compdb", "no_compdb.json"])
        self.assert_exit_code(cindex_dump.main, "Failed to load compdb")

    def test_file_and_compdb_file_not_in_compdb(self):
        test_support.set_arguments(["--file", self.existing_file, "--compdb", self.existing_compdb])
        self.assert_exit_code(cindex_dump.main, "not found in compdb")

    def test_valid_but_missing_file(self):
        test_support.set_arguments(["--file", "not_existing.cpp"])
        self.assert_exit_code(cindex_dump.main, "Unable to load input for file 'not_existing.cpp'")

    def test_valid_existing_file(self):
        test_support.set_arguments(["--file", self.existing_file])
        self.assert_exit_code(cindex_dump.main, 0)


if __name__ == "__main__":
    test_support.default_test_setup()
