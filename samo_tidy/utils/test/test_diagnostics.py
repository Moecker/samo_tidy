import unittest

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.test.test_support as test_support
import samo_tidy.utils.diagnostics as diagnostics


class TestDiagnostics(unittest.TestCase):
    def test_get_diagnostics_by_severity_one_tu(self):
        source_file = test_support.create_tempfile(["int a;"])
        translation_unit = tu_parser.create_translation_unit(source_file)
        self.assertTrue(translation_unit)

        diags = diagnostics.get_diagnostics_by_severity_one_tu(translation_unit)
        self.assertEqual(diags["2"], 1)

    def test_one_severity_3_one_severity_2(self):
        source_file = test_support.create_tempfile(["int8 a;", "int b;"])
        translation_unit = tu_parser.create_translation_unit(source_file)
        self.assertTrue(translation_unit)

        diags = diagnostics.get_diagnostics_by_severity(translation_unit)
        self.assertEqual(diags[source_file]["3"], 1)
        self.assertEqual(diags[source_file]["2"], 1)

    def test_two_severity_3(self):
        source_file = test_support.create_tempfile(["int8 a;", "int8 b;"])
        translation_unit = tu_parser.create_translation_unit(source_file)
        self.assertTrue(translation_unit)

        diags = diagnostics.get_diagnostics_by_severity(translation_unit)
        self.assertEqual(diags[source_file]["3"], 2)


if __name__ == "__main__":
    test_support.default_test_setup()
