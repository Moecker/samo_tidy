import unittest
import logging

import samo_tidy.test.test_utils as test_utils


class TestFacade(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)


if __name__ == "__main__":
    test_utils.default_test_setup()
