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
import samo_tidy.fixit.fixit as fixit
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.logger as logger
import samo_tidy.utils.utils as utils


def apply_checkers_for_commands(commands, the_config):
    translation_units = compdb_parser.parse_commands(commands, the_config.files)
    return apply_checkers_for_translation_units(translation_units, the_config)


def apply_checkers_for_translation_units(translation_units, the_config):
    all_violations = []
    for translation_unit in translation_units:
        all_violations += apply_checkers_for_translation_unit(translation_unit, the_config)

    # TODO Integrate this better and only if --fix option is active
    # import samo_tidy.checker.samo_suffix_case_checker as samo_suffix_case_checker
    # fixit.fix_violations(all_violations, samo_suffix_case_checker.fix)

    return all_violations


def apply_checkers_for_translation_unit(translation_unit, the_config):
    violations_per_tu = []
    # For each translation unit, apply the checkers
    # TODO Do not differentiation between tu and token based checker
    if translation_unit:
        logging.info(colored("Applying checkers for '%s'", "magenta"), utils.only_filename(translation_unit.spelling))
        summary.get_summary().add_translation_unit(translation_unit.spelling)

        # Apply the checker
        for the_checker in the_config.active_checkers:
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
    return violations_per_tu


def parse_args():
    parser = argparse.ArgumentParser("Samo Tidy", formatter_class=RawTextHelpFormatter)
    parser.add_argument("--compdb", required=True, help="Directory which contains the 'compile_comands.json' file")
    parser.add_argument(
        "--files",
        nargs="+",
        help=(
            "List of files from compdb to be analyzed. Treated as substrings. Default: All files\n"
            "Example: '--files .cpp' would match every file which has '.cpp' in its name"
        ),
        default=None,
    )
    # TODO Implement this
    parser.add_argument(
        "--checkers",
        nargs="+",
        help=(
            "List of checkers to be applied. Treated as substrings. Default: All checkers\n"
            "Example: '--checkers SAMO_TIDY_SUFFIX' would apply every checker which has 'SAMO_TIDY_SUFFIX' in its name"
        ),
        default=None,
    )
    # TODO Implement this
    parser.add_argument(
        "--fix", help="Apply fixes. Caution! This will change source files", action="store_true", default=False
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


def run(runner, the_config):
    compdb = compdb_parser.load_compdb(the_config.compdb)
    the_summary = summary.get_summary()
    if compdb:
        the_summary = runner(the_config, compdb)
    else:
        logging.error("Could not load compdb")
        sys.exit("Loading of compdb failed")
    return the_summary


# Entry point for serial and parallel runner
def main(runner):
    args = parse_args()

    the_config = config.Config(
        active_checkers=config.ALL_CHECKERS,
        compdb=args.compdb,
        files=args.files,
        log_level=args.log_level,
        workers=args.workers,
        fix=args.fix,
    )

    logger.setup_logger(args.log_level, args.log_file)
    logging.critical(colored("Welcome. Lets run some static code analysis checks...", "magenta"))

    clang_setup.setup_clang()

    the_summary = run(runner, the_config)

    logging.critical(colored("SUMMARY:\n" + pformat(the_summary.present()), attrs=["dark"]))

    sys.exit(0)
