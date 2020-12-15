import unittest

import samo_tidy.test.test_support as test_support
import samo_tidy.utils.utils as utils


class TestUtils(unittest.TestCase):
    def test_shall_ignore_based_on_file_name(self):
        self.assertTrue(utils.shall_ignore_based_on_file_name("/usr/foo.cpp"))
        self.assertTrue(utils.shall_ignore_based_on_file_name("/tmp/usr/ignore_me.cpp"))
        self.assertFalse(utils.shall_ignore_based_on_file_name("foo.cpp"))


if __name__ == "__main__":
    test_support.default_test_setup()
