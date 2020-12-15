import argparse
from argparse import RawTextHelpFormatter
from pprint import pformat
from termcolor import colored

import logging
import sys

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.summary as summary

import samo_tidy.checker.checker as checker
import samo_tidy.checker.clang_warning_checker as clang_warning_checker

import samo_tidy.utils.utils as utils
import samo_tidy.utils.logger as logger

import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.samo_unsigned_int_checker as samo_unsigned_int_checker

active_checkers = [
    samo_suffix_case_checker.token_based_rule,
    samo_unsigned_int_checker.token_based_rule,
    samo_multiple_classes_checker.translation_unit_based_rule,
]


def get_checker_registry():
    registry = set(active_checkers)
    return registry


def apply_checkers_for_translation_units(translation_units):
    number_of_successfull_tus = 0
    # For each translation unit, apply the checkers
    # TODO Do not differentiation between tu and token based checker
    for translation_unit in translation_units:
        if translation_unit:
            logging.info(
                colored("Applying checkers for '%s'", "magenta"), utils.only_filename(translation_unit.spelling)
            )
            summary.add_translation_unit(translation_unit.spelling)

            # Apply the checker
            for the_checker in get_checker_registry():
                checker.apply_checker(translation_unit, the_checker)

            # Always apply the clang warning checker
            clang_warning_checker.check_for_clang_warnings(translation_unit)
            number_of_successfull_tus += 1
        else:
            logging.warning("Skipping invalid translation unit")
    return number_of_successfull_tus


def run(compdb_root_dir, files=None):
    compdb = compdb_parser.load_compdb(compdb_root_dir)
    if compdb:
        translation_units = compdb_parser.parse_compdb(compdb, files)
    else:
        logging.error("Could not load compdb")
        sys.exit("Loading of compdb failed")
    apply_checkers_for_translation_units(translation_units)


def main():
    parser = argparse.ArgumentParser("SAMO TIDY", formatter_class=RawTextHelpFormatter)
    parser.add_argument("--compdb", required=True, help="Directory which contains the 'compile_comands.json' file")
    parser.add_argument(
        "--files",
        nargs="+",
        help=(
            "List of files from compdb to be analyzed. Used substring search.\n"
            "Example: '--files .cpp' would match every file which has '.cpp' in its name"
        ),
    )
    parser.add_argument("--log_file", help="Full path to a log file")
    parser.add_argument("--log_level", help="Log level. One of {DEBUG, INFO, WARN, ERROR}")

    args = parser.parse_args()

    logger.setup_logger(args.log_level, args.log_file)
    logging.info(colored("Welcome", "magenta"))
    utils.setup_clang()
    run(args.compdb, args.files)

    logging.info("SUMMARY:\n" + pformat(summary.present()))

    sys.exit(0)


if __name__ == "__main__":
    main()
