import unittest
import logging
import os
import shutil
import tempfile

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.utils.utils as utils


def create_temp_file_for(compdb_string, dir, name):
    desired_path = os.path.join(dir, name)
    with tempfile.NamedTemporaryFile(dir=dir, delete=False) as tmp:
        logging.debug("Writing compilation database to: '%s'", desired_path)
        with open(tmp.name, "w") as f:
            f.write(compdb_string)
        shutil.copy(tmp.name, desired_path)
        utils.debug_file_content(desired_path)


def create_compdb_string(directory, command, the_file):
    inner = f'"directory": "{directory}", "command": "{command}", "file": "{the_file}"'
    return "[{" + inner + "}]"


class TestCoreLib(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "../../test/data")
        self.temporary_dir = "/tmp"
        self.compdb_name = "compile_commands.json"
        self.compdb_full_path = os.path.join(self.temporary_dir, self.compdb_name)

    def tearDown(self):
        if os.path.exists(self.compdb_full_path):
            os.remove(self.compdb_full_path)

    def create_and_parse_comdb(self, file_name):
        self.create_temporary_compdb_file(file_name)
        compdb = compdb_parser.load_compdb(directory=self.temporary_dir)
        return compdb

    def create_temporary_compdb_file(self, file_name):
        compdb = create_compdb_string(self.test_data_dir, "c++", file_name)
        create_temp_file_for(compdb, self.temporary_dir, self.compdb_name)
