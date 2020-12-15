import unittest
import os

import samo_tidy.facade.parallel_facade as parallel_facade

import samo_tidy.test.test_support as test_support


class TestFacade(unittest.TestCase):
    def test_apply_checkers_for_translation_units(self):
        test_data_dir = os.path.join(os.path.dirname(__file__), "../../test/data/multiple_files_compdb")
        result = parallel_facade.run_parallel(test_data_dir)


if __name__ == "__main__":
    test_support.default_test_setup()
