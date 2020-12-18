import unittest

import samo_tidy.fixit.fixit as fixit
import samo_tidy.test.test_support as test_support


class TestFacade(unittest.TestCase):
    def test_missing_arguments(self):
        self.assertTrue(True)


if __name__ == "__main__":
    test_support.default_test_setup()
