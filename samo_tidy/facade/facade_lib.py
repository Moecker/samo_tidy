from argparse import RawTextHelpFormatter
from pprint import pformat
from termcolor import colored
import argparse
import logging
import sys
import multiprocessing

import samo_tidy.checker.checker as checker
import samo_tidy.checker.clang_warning_checker as clang_warning_checker
import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.checker.samo_unsigned_int_checker as samo_unsigned_int_checker
import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.logger as logger
import samo_tidy.utils.utils as utils

active_checkers = [
    samo_suffix_case_checker.token_based_rule,
    samo_unsigned_int_checker.token_based_rule,
    samo_multiple_classes_checker.translation_unit_based_rule,
]


def get_checker_registry():
    registry = set(active_checkers)
    return registry


def run_for_translation_unit(translation_unit):
    # For each translation unit, apply the checkers
    # TODO Do not differentiation between tu and token based checker
    if translation_unit:
        logging.info(colored("Applying checkers for '%s'", "magenta"), utils.only_filename(translation_unit.spelling))
        summary.add_translation_unit(translation_unit.spelling)

        # Apply the checker
        for the_checker in get_checker_registry():
            checker.apply_checker(translation_unit, the_checker)

        # Always apply the clang warning checker
        clang_warning_checker.check_for_clang_warnings(translation_unit)
    else:
        logging.warning("Skipping invalid translation unit")
    return summary


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
    the_summary = summary.Summary
    if compdb:
        the_summary = runner(compdb, log_level, workers, files)
    else:
        logging.error("Could not load compdb")
        sys.exit("Loading of compdb failed")
    return the_summary


def main(runner):
    args = parse_args()

    logger.setup_logger(args.log_level, args.log_file)
    logging.info(colored("Welcome", "magenta"))

    clang_setup.setup_clang()

    the_summary = run(runner, args.compdb, args.log_level, args.workers, args.files)

    logging.info("SUMMARY:\n" + pformat(the_summary.present()))

    sys.exit(0)
