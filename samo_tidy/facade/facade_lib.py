from argparse import RawTextHelpFormatter
from pprint import pformat
from termcolor import colored
import argparse
import logging
import multiprocessing
import sys

import samo_tidy.checker.checker as checker
import samo_tidy.checker.clang_warning_checker as clang_warning_checker
import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary
import samo_tidy.facade.config as config
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.logger as logger
import samo_tidy.utils.utils as utils


def run_all(commands, files):
    translation_units = compdb_parser.parse_commands(commands, files)
    apply_checkers_for_translation_units(translation_units)


def apply_checkers_for_translation_units(translation_units):
    for translation_unit in translation_units:
        run_for_translation_unit(translation_unit)


def run_for_translation_unit(translation_unit):
    violations_per_tu = []
    # For each translation unit, apply the checkers
    # TODO Do not differentiation between tu and token based checker
    if translation_unit:
        logging.info(colored("Applying checkers for '%s'", "magenta"), utils.only_filename(translation_unit.spelling))
        summary.get_summary().add_translation_unit(translation_unit.spelling)

        # Apply the checker
        for the_checker in config.get_checker_registry():
            violations_per_tu += checker.apply_checker(translation_unit, the_checker)

        # Always apply the clang warning checker
        clang_warnings = clang_warning_checker.check_for_clang_warnings(translation_unit)
        logging.critical(
            colored("Translation Unit '%s' has %d violation(s) and %d clang warning(s)", "red"),
            utils.only_filename(translation_unit.spelling),
            len(violations_per_tu),
            len(clang_warnings),
        )
        summary.get_summary().add_number_of_violations((len(violations_per_tu), len(clang_warnings)))
    else:
        logging.warning("Skipping invalid translation unit")


def parse_args():
    parser = argparse.ArgumentParser("Samo Tidy", formatter_class=RawTextHelpFormatter)
    parser.add_argument("--compdb", required=True, help="Directory which contains the 'compile_comands.json' file")
    parser.add_argument(
        "--files",
        nargs="+",
        help=(
            "List of files from compdb to be analyzed. Used substring search. Default: All files\n"
            "Example: '--files .cpp' would match every file which has '.cpp' in its name"
        ),
        default=None,
    )
    parser.add_argument("--log_file", help="Full path to a log file", default=None)
    parser.add_argument(
        "--log_level", help="Log level. One of {DEBUG, INFO, WARN, ERROR}. Default: INFO", default="info"
    )
    parser.add_argument(
        "--workers",
        help="Number of workers for parallel execution. Default: Number of CPUs - 1",
        type=int,
        default=multiprocessing.cpu_count() - 1,
    )

    args = parser.parse_args()
    return args


def run(runner, compdb_root_dir, log_level, workers, files=[]):
    compdb = compdb_parser.load_compdb(compdb_root_dir)
    the_summary = summary.get_summary()
    if compdb:
        the_summary = runner(compdb, log_level, workers, files)
    else:
        logging.error("Could not load compdb")
        sys.exit("Loading of compdb failed")
    return the_summary


def main(runner):
    args = parse_args()

    logger.setup_logger(args.log_level, args.log_file)
    logging.critical(colored("Welcome. Lets run some static code analysis checks...", "magenta"))

    clang_setup.setup_clang()

    the_summary = run(runner, args.compdb, args.log_level, args.workers, args.files)

    logging.critical(colored("SUMMARY:\n" + pformat(the_summary.present()), attrs=["dark"]))

    sys.exit(0)
