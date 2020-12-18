from pathlib import Path
import collections
import coverage
import logging
import sys
import unittest

Result = collections.namedtuple("Result", "runs errors failures")


def invoke_coverage(*deps):
    cov = coverage.Coverage(branch=True, omit="*/external/*")

    cov.start()

    loader = unittest.TestLoader()
    all_tests_suite = unittest.TestSuite()

    for dep in deps:
        if ":" in dep:
            target_name_of_label = dep.rpartition(":")[2]
        else:
            target_name_of_label = dep.rpartition("/")[2]

        pathes = list(Path(".").glob(f"**/{target_name_of_label}"))
        suite = loader.discover(start_dir=pathes[0].parent, pattern="*test*.py")
        all_tests_suite.addTests(suite)

    runner = unittest.TextTestRunner()
    result = runner.run(all_tests_suite)

    cov.stop()
    cov.save()
    cov.report()

    results = Result(runs=result.testsRun, errors=len(result.errors), failures=len(result.failures))
    logging.info("Runs: %s, Errors %s, Failures: %s", results.runs, results.errors, results.failures)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("unittest").setLevel(logging.FATAL)
    invoke_coverage(*sys.argv[1:])
