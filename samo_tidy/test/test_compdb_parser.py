import unittest
import logging
import os
import shutil
import tempfile

from unittest import skip

from samo_tidy.core.compdb_parser import load_compdb, parse_compdb
from samo_tidy.utils.utils import debug_file_content
from samo_tidy.test.test_utils import default_test_setup


def create_temp_file_for(compdb_string, dir, name):
    desired_path = os.path.join(dir, name)
    with tempfile.NamedTemporaryFile(dir=dir, delete=False) as tmp:
        logging.debug("Writing compilation database to: '%s'", desired_path)
        with open(tmp.name, "w") as f:
            f.write(compdb_string)
        shutil.copy(tmp.name, desired_path)
        debug_file_content(desired_path)


def create_compdb_string(directory, command, the_file):
    inner = f'"directory": "{directory}", "command": "{command}", "file": "{the_file}"'
    return "[{" + inner + "}]"


class TestClang(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")
        self.temporary_dir = "/tmp"
        self.compdb_name = "compile_commands.json"
        self.compdb_full_path = os.path.join(self.temporary_dir, self.compdb_name)

    def tearDown(self):
        if os.path.exists(self.compdb_full_path):
            os.remove(self.compdb_full_path)

    def create_temporary_compdb_file(self, file_name):
        compdb = create_compdb_string(self.test_data_dir, "c++", file_name)
        create_temp_file_for(compdb, self.temporary_dir, self.compdb_name)

    def test_load_load_compdb_success(self):
        self.create_temporary_compdb_file("source_id1.cpp")
        compdb = load_compdb(directory=self.temporary_dir)
        self.assertTrue(compdb != None)

    def test_load_load_compdb_fail(self):
        compdb = load_compdb(directory=self.temporary_dir)
        self.assertTrue(compdb == None)

    def test_parse_compdb(self):
        self.create_temporary_compdb_file("source_id1.cpp")
        compdb = load_compdb(directory=self.temporary_dir)
        translation_units = parse_compdb(compdb)
        self.assertEqual(len(translation_units), 1)
        self.assertIn("source_id1.cpp", translation_units[0].spelling)


if __name__ == "__main__":
    default_test_setup()