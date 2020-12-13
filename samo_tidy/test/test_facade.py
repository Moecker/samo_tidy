import unittest
import logging

from samo_tidy.test.test_utils import default_test_setup


class TestFacade(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)


if __name__ == "__main__":
    default_test_setup()