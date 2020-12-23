import unittest

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.test.test_core_lib as test_core_lib
import samo_tidy.test.test_support as test_support


class TestCompdbParser(test_core_lib.TestCoreLib):
    def test_load_compdb_parser_success(self):
        compdb = self.create_and_parse_comdb(["source_id1.cpp"])
        self.assertTrue(compdb != None)

    def test_load_compdb_parser_compdb_fail(self):
        compdb = compdb_parser.load_compdb(directory=self.temporary_dir)
        self.assertTrue(compdb == None)

    def test_parse_compdb(self):
        compdb = self.create_and_parse_comdb(["source_id1.cpp"])
        translation_units = self.parse_compdb(compdb)
        self.assertEqual(len(translation_units), 1)
        self.assertIn("source_id1.cpp", translation_units[0].spelling)

    def test_parse_compdb_set_of_files(self):
        compdb = self.create_and_parse_comdb(["source_id2.cpp"])
        translation_units = self.parse_compdb(compdb, ["source_id2.cpp"])
        self.assertEqual(len(translation_units), 1)
        self.assertIn("source_id2.cpp", translation_units[0].spelling)

    def test_parse_compdb_multiple_files(self):
        compdb = self.create_and_parse_comdb(["source_id1.cpp", "source_id2.cpp"])
        translation_units = self.parse_compdb(compdb)
        self.assertEqual(len(translation_units), 2)
        self.assertIn("source_id1.cpp", translation_units[0].spelling)
        self.assertIn("source_id2.cpp", translation_units[1].spelling)

    def test_parse_compdb_set_of_files_missing(self):
        compdb = self.create_and_parse_comdb(["source_id2.cpp"])
        translation_units = self.parse_compdb(compdb, ["not_existing"])
        self.assertEqual(len(translation_units), 0)

    def test_parse_compdb_ignore_file_name(self):
        compdb = self.create_and_parse_comdb(["external/ignored.cpp"])
        translation_units = self.parse_compdb(compdb)
        self.assertEqual(len(translation_units), 0)

    def test_parse_compdb_ignore_file_name_ok(self):
        compdb = self.create_and_parse_comdb(["internal/not_ignored.cpp"])
        translation_units = self.parse_compdb(compdb)
        self.assertEqual(len(translation_units), 1)
        self.assertEqual(translation_units[0], None)


if __name__ == "__main__":
    test_support.default_test_setup()
