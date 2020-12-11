import unittest
from unittest import skip
import logging
import os
import shutil


from samo_tidy.core.clang import (
    foo,
    setup,
    load_compilation_db,
    parse_compilation_database,
)


import tempfile


def create_temp_file_for(compilation_database_string, dir):
    with tempfile.NamedTemporaryFile(dir=dir, delete=False) as tmp:
        print(tmp.name)
        shutil.copy(tmp.name, dir + "/compile_commands.json")
        print(os.listdir(dir))
        compilation_database_string_as_bytes = bytes(
            compilation_database_string, "utf-8"
        )
        tmp.write(compilation_database_string_as_bytes)


def create_compilation_database_string(directory, command, file):
    inner = f'["directory": "{directory}", "command": "{command}", "file": "{file}"]'
    return "{" + inner + "}"


class TestClang(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")

    def test_foo(self):
        self.assertEqual("foo", foo())

    def test_setup(self):
        setup()
        compilation_database = load_compilation_db(
            "/Users/q367607/Github/samo_tidy/cpp_sources/build"
        )
        parse_compilation_database(compilation_database)

    def test_compilation_commands_parsing(self):
        setup()
        dir = "/tmp"
        compilation_database = create_compilation_database_string("foo", "bar", "blub")
        file_name = os.path.join(self.test_data_dir, "foo.cpp")
        compilation_database = create_compilation_database_string(
            self.test_data_dir, "c++", file_name
        )
        create_temp_file_for(compilation_database, dir)
        print(compilation_database)
        compilation_database = load_compilation_db(directory=dir)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()