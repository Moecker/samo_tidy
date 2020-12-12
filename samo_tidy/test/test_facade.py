import unittest
import logging


class TestFacade(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()