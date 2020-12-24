import time
import unittest

import samo_tidy.test.test_support as test_support
import samo_tidy.utils.parallel as parallel
import samo_tidy.utils.utils as utils


class TestParallel(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.the_list = [0, 1, 2, 3, 4, 5, 6, 7]

    def test_dummy_parallel_1_worker(self):
        output = parallel.execute_parallel(self.the_list, 1, computation)
        self.assertEqual(len(output), 8)

    def test_dummy_parallel_2_workers_single_list_entry(self):
        output = parallel.execute_parallel([10], 2, computation)
        self.assertEqual(len(output), 1)
        self.assertEqual(output, [100])

    def test_dummy_parallel_4_worker(self):
        output = parallel.execute_parallel(self.the_list, 4, computation)
        self.assertEqual(len(output), 8)
        self.assertEqual(output, [0, 1, 4, 9, 16, 25, 36, 49])


def computation(args):
    start, end, the_list, _ = args
    ret = []

    for i in range(start, end):
        ret.append(the_list[i] * the_list[i])
        time.sleep(0.01)
    return ret


if __name__ == "__main__":
    test_support.default_test_setup()
