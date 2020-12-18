import unittest
from clang import cindex

import samo_tidy.test.test_support as test_support


class TestDump(unittest.TestCase):
    def test_pretty_location(self):
        # TODO One cannot really instantiate binding classes
        location = cindex.SourceLocation()
        self.assertTrue(True)


if __name__ == "__main__":
    test_support.default_test_setup()
