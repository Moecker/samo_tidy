import itertools
import multiprocessing


def execute_parallel(the_list, workers, the_function, function_args=()):
    list_length = len(the_list)
    if list_length == 0:
        return []

    workers = min(workers, list_length)
    batch = int(list_length / workers)

    output = []
    with multiprocessing.Pool(workers) as pool:
        output = pool.map(
            the_function,
            [
                (start, min(start + batch, list_length), the_list, function_args)
                for start in range(
                    0,
                    list_length,
                    batch,
                )
            ],
        )
    return list(itertools.chain.from_iterable(output))
