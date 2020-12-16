import os
import unittest

import samo_tidy.facade.facade_lib as facade_lib
import samo_tidy.facade.parallel_facade as parallel_facade
import samo_tidy.facade.test.test_facade_lib as test_facade_lib
import samo_tidy.test.test_support as test_support


class TestParallelFacade(test_facade_lib.TestFacadeLib):
    def test_default_arguments_valid_but_empty_db(self):
        self.set_arguments(
            ["--compdb", self.multiple_compdb_root, "--log_level", test_support.get_default_log_level_for_tests()]
        )
        self.assert_exit_code(parallel_facade.main, 0)

    def test_apply_checkers_for_translation_units(self):
        result = facade_lib.run(
            parallel_facade.run_parallel, self.multiple_compdb_root, test_support.get_default_log_level_for_tests(), 2
        )
        # TODO Expect results in summary module

    def test_apply_checkers_for_single_entry(self):
        result = facade_lib.run(
            parallel_facade.run_parallel, self.single_compdb_root, test_support.get_default_log_level_for_tests(), 1
        )


if __name__ == "__main__":
    test_support.default_test_setup()
