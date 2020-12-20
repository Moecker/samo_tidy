from pathlib import Path
import collections
import coverage
import logging
import os
import sys
import unittest

Result = collections.namedtuple("Result", "runs errors failures")


def invoke_coverage(*deps):
    """Employs coverage API to measure code coverage for all targets given in deps"""
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

    # TODO Do not hardcode the output location
    directory = os.path.join("/tmp", "coverage", target_name_of_label)
    xml_report = os.path.join(directory, "coverage.xml")
    html_report = os.path.join(directory, "index.html")
    cov.xml_report(outfile=xml_report)
    cov.html_report(directory=directory)
    logging.info("Coverage XML report written to file://%s", xml_report)
    logging.info("Coverage HTML report written to file://%s", html_report)

    results = Result(runs=result.testsRun, errors=len(result.errors), failures=len(result.failures))
    logging.info("Runs: %s, Errors %s, Failures: %s", results.runs, results.errors, results.failures)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("unittest").setLevel(logging.FATAL)
    invoke_coverage(*sys.argv[1:])
