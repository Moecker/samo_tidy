import unittest

import samo_tidy.core.summary as summary
import samo_tidy.test.test_support as test_support


class TestSummary(unittest.TestCase):
    def test_merge_multiple_entries(self):
        the_summary1 = summary.Summary()
        the_summary2 = summary.Summary()
        the_summary1.add_analyzed_translation_unit("tu1.cpp")
        the_summary2.add_analyzed_translation_unit("tu2.cpp")
        new_summary = summary.merge([the_summary1, the_summary2])
        self.assertEqual(len(new_summary.analyzed_translation_units), 2)
        self.assertIn("tu1.cpp", new_summary.analyzed_translation_units)
        self.assertIn("tu2.cpp", new_summary.analyzed_translation_units)

    def test_merge_single_entry(self):
        the_summary = summary.Summary()
        the_summary.add_analyzed_translation_unit("tu.cpp")
        new_summary = summary.merge([the_summary, the_summary])
        self.assertEqual(len(new_summary.analyzed_translation_units), 1)
        self.assertIn("tu.cpp", new_summary.analyzed_translation_units)


if __name__ == "__main__":
    test_support.default_test_setup()
