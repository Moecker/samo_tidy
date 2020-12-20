import itertools
import multiprocessing


def execute_parallel(the_list, workers, the_function, function_args=()):
    """Uses map-reduce to equally load entries of the_list into multiple workers runing the_function with given args"""
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
                # For each worker: Run on the_list from start to the end of the next batch
                (start, min(start + batch, list_length), the_list, function_args)
                for start in range(
                    0,
                    list_length,
                    batch,
                )
            ],
        )
    # Combined the lists of list for each worker into a single list
    return list(itertools.chain.from_iterable(output))
