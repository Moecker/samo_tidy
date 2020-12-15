import unittest
import time

import samo_tidy.core.parallel_parser as parallel_parser
import samo_tidy.utils.utils as utils

import samo_tidy.core.test.test_core_lib as test_core_lib
import samo_tidy.test.test_support as test_support


def computation(args):
    start, end, the_list = args
    ret = []

    for i in range(start, end):
        ret.append(the_list[i] * the_list[i])
        time.sleep(0.01)
    return ret


class TestClang(test_core_lib.TestCoreLib):
    def setUp(self):
        super().setUp()
        self.the_list = [0, 1, 2, 3, 4, 5, 6, 7]

    def test_dummy_parallel_4_worker(self):
        output = utils.parallel(self.the_list, 4, computation)
        self.assertEqual(len(output), 8)
        self.assertEqual(output, [0, 1, 4, 9, 16, 25, 36, 49])

    def test_dummy_parallel_1_worker(self):
        output = utils.parallel(self.the_list, 1, computation)
        self.assertEqual(len(output), 8)

    def test_parallel_parse_compdb(self):
        compdb = self.create_and_parse_comdb(["source_id1.cpp"])
        translation_units = parallel_parser.parallel_parse_compdb(compdb)
        self.assertEqual(len(translation_units), 1)


if __name__ == "__main__":
    test_support.default_test_setup()
