import unittest

import samo_tidy.fixit.fixit as fixit
import samo_tidy.test.test_support as test_support
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
from samo_tidy.checker.violation import Violation


class TestFacade(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

    def test_fixit(self):
        filename = test_support.create_tempfile(["std::uint8_t var = 1u;"])
        violation = Violation("TIDY_SAMO_SUFFIX_CASE", "", filename, 0, 20)

        samo_suffix_case_checker.fixit(violation)
        with open(violation.file_path) as the_file:
            self.assertEqual(the_file.readlines()[violation.line].strip(), "std::uint8_t var = 1U;")


if __name__ == "__main__":
    test_support.default_test_setup()
