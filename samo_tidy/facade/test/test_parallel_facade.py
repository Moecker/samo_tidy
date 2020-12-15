import unittest
import os

import samo_tidy.facade.parallel_facade as parallel_facade
import samo_tidy.facade.facade_lib as facade_lib
import samo_tidy.test.test_support as test_support
import samo_tidy.facade.test.test_facade_lib as test_facade_lib


class TestParallelFacade(test_facade_lib.TestFacade):
    def test_default_arguments_valid_but_empty_db(self):
        self.set_arguments(["--compdb", self.test_data_dir])
        self.assert_exit_code(parallel_facade.main, 0)

    def test_apply_checkers_for_translation_units(self):
        result = facade_lib.run(parallel_facade.run_parallel, self.test_data_dir)


if __name__ == "__main__":
    test_support.default_test_setup()
