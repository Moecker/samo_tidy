import unittest
import logging

from samo_tidy.utils.utils import setup_clang


def default_test_setup():
    logging.basicConfig(level=logging.DEBUG)
    setup_clang()
    unittest.main()