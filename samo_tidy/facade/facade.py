import argparse
from argparse import RawTextHelpFormatter

import logging
import sys

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.checker.checker as checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.clang_warning_checker as clang_warning_checker
import samo_tidy.utils.utils as utils


def apply_checkers_for_translation_units(translation_units):
    for tu in translation_units:
        if tu:
            checker.apply_checker(tu, samo_suffix_case_checker.rule)
            checker.apply_checker(tu, samo_multiple_classes_checker.rule)
            clang_warning_checker.check_for_clang_warnings(tu)
        else:
            logging.warning("Skipping translation unit")


def run(compdb_root_dir, files=None):
    compdb = compdb_parser.load_compdb(compdb_root_dir)
    if compdb:
        translation_units = compdb_parser.parse_compdb(compdb, files)
    else:
        logging.error("Could not load compdb")
        sys.exit("Loading of compdb failed")
    apply_checkers_for_translation_units(translation_units)


def setup_logger(log_file, loglevel):
    the_logger = logging.getLogger()

    if loglevel:
        level = getattr(logging, loglevel.upper(), None)
        if not isinstance(level, int):
            raise ValueError("Invalid log level: %s" % loglevel)
    else:
        level = logging.INFO

    formater = logging.Formatter("[%(levelname)-7.7s] %(message)s")
    the_logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formater)
    the_logger.addHandler(console_handler)

    if log_file:
        file_handler = logging.FileHandler(
            log_file,
            "w",
        )
        file_handler.setFormatter(formater)
        the_logger.addHandler(file_handler)


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

    setup_logger(args.log_file, args.log_level)

    utils.setup_clang()
    run(args.compdb, args.files)


if __name__ == "__main__":
    main()
