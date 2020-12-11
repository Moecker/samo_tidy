import unittest
from samo_tidy.core.run import foo


class TestRun(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

    def test_foo(self):
        self.assertEqual("foo", foo())


if __name__ == "__main__":
    unittest.main()