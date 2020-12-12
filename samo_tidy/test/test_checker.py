import unittest
from unittest import skip
import clang
import os
import logging
from pprint import pformat
import tempfile
import shutil
from clang import cindex

from samo_tidy.checker.checker import check_for_ints
from samo_tidy.utils.utils import debug_file_content, setup_clang, get_diag_info
from samo_tidy.utils.cindex_dump import get_info


def create_translation_unit(source_file, args=[]):
    index = cindex.Index.create()
    logging.debug("Using args: %s", args)
    logging.debug("Using source_file: %s", source_file)
    tu = index.parse(source_file, args=args)
    logging.info(pformat(("diags", [get_diag_info(d) for d in tu.diagnostics])))
    return tu


def make_file_string(the_list):
    return "\n".join(the_list)


def create_temp_file_for(content):
    the_string = make_file_string(content)
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        desired_name = tmp.name + ".cpp"
        logging.debug("Writing file to: %s", tmp.name)
        with open(tmp.name, "w") as f:
            f.write(the_string)
        shutil.copy(tmp.name, desired_name)
        debug_file_content(desired_name)
    return desired_name


class TestChecker(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), "data")

    def get_source_file_path(self, file_name):
        source_file = os.path.join(self.test_data_dir, file_name)
        return source_file

    def check_ints(self, source_file, args=[]):
        tu = create_translation_unit(source_file, args)
        violations = check_for_ints(tu)
        return violations, tu.diagnostics

    def dump(self, source_file, args=[]):
        tu = create_translation_unit(source_file, args)
        logging.debug(pformat(("nodes", get_info(tu.cursor))))

    def test_check_for_ints_id1(self):
        source_file = self.get_source_file_path("source_id1.cpp")
        violations, diagnostics = self.check_ints(source_file)
        self.assertEqual(len(violations), 1)
        self.assertEqual(len(diagnostics), 0)
        self.assertIn("source_id1.cpp", violations[0].file)
        self.assertEqual("TIDY_SUFFIX_CASE", violations[0].id)

    def test_check_for_ints_id2(self):
        source_file = self.get_source_file_path("source_id2.cpp")
        violations, diagnostics = self.check_ints(source_file)
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(diagnostics), 0)

    def test_check_for_ints_id3(self):
        source_file = self.get_source_file_path("source_id3.cpp")
        tu = create_translation_unit(source_file)
        self.assertEqual(len(tu.diagnostics), 1)
        self.assertIn("expected ';'", tu.diagnostics[0].spelling)

    def test_check_for_ints_id4(self):
        source_file = self.get_source_file_path("source_id4.cpp")
        violations, diagnostics = self.check_ints(source_file, [f"-I{self.test_data_dir}"])
        self.assertEqual(len(violations), 0)
        self.assertEqual(len(diagnostics), 0)

    def test_temp_file_int(self):
        content = ["int Function()", "{", "return 0;", "}"]
        file_name = create_temp_file_for(content)
        violations, diagnostics = self.check_ints(file_name)
        self.assertEqual(len(violations), 0)

    def test_temp_file_uint(self):
        content = ["#include <cstdint>", "std::uint8_t Function()", "{", "return 0u;", "}"]
        file_name = create_temp_file_for(content)
        violations, diagnostics = self.check_ints(file_name)
        self.assertEqual(len(violations), 1)
        self.assertIn(file_name, violations[0].file)
        self.assertEqual("TIDY_SUFFIX_CASE", violations[0].id)

    @skip("No yet supported")
    def test_temp_file_uint_def(self):
        content = ["#include <cstdint>", "std::uint8_t a = 1;"]
        file_name = create_temp_file_for(content)
        violations, diagnostics = self.check_ints(file_name)
        self.dump(file_name)
        self.assertEqual(len(violations), 1)
        self.assertIn(file_name, violations[0].file)
        self.assertEqual("TIDY_SUFFIX_MISSING", violations[0].id)

    @skip("No yet supported")
    def test_temp_file_uint_missing(self):
        content = ["#include <cstdint>", "std::uint8_t Function()", "{", "return 0;", "}"]
        file_name = create_temp_file_for(content)
        violations, diagnostics = self.check_ints(file_name)
        self.assertEqual(len(violations), 1)
        self.assertIn(file_name, violations[0].file)
        self.assertEqual("TIDY_SUFFIX_MISSING", violations[0].id)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    setup_clang()
    unittest.main()