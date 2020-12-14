import argparse
from argparse import RawTextHelpFormatter

import logging
import sys

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.checker.checker as checker
import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
import samo_tidy.checker.samo_multiple_classes_checker as samo_multiple_classes_checker
import samo_tidy.checker.samo_unsigned_int_checker as samo_unsigned_int_checker
import samo_tidy.checker.clang_warning_checker as clang_warning_checker
import samo_tidy.utils.utils as utils
import samo_tidy.utils.logger as logger


def apply_checkers_for_translation_units(translation_units):
    for tu in translation_units:
        logging.info("Applying checkers for '%s'", utils.only_filename(tu.spelling))
        if tu:
            checker.apply_checker(tu, samo_suffix_case_checker.rule)
            checker.apply_checker(tu, samo_multiple_classes_checker.rule)
            checker.apply_checker(tu, samo_unsigned_int_checker.rule)
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

    utils.setup_clang()
    run(args.compdb, args.files)
    sys.exit(0)


if __name__ == "__main__":
    main()
