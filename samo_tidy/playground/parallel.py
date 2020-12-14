import multiprocessing
import itertools
import time


def computation(args):
    start, end, the_list = args
    ret = []

    for i in range(start, end):
        ret.append(the_list[i] * 100)
        time.sleep(0.1)
    return ret


def parallel(the_list, workers, the_function):
    list_length = len(the_list)
    workers = min(workers, list_length)
    batch = int(list_length / workers)

    output = []
    with multiprocessing.Pool(workers) as pool:
        output = pool.map(
            the_function,
            [
                (start, min(start + batch, list_length), the_list)
                for start in range(
                    0,
                    list_length,
                    batch,
                )
            ],
        )
    return list(itertools.chain.from_iterable(output))


def main():
    the_list = 2 * [0, 1, 2, 3, 4, 5, 6, 7]
    output = parallel(the_list, 4, computation)
    print(output)


if __name__ == "__main__":
    main()
