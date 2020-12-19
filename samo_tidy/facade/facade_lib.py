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
    """For each extarcted command from comdb, apply checkers"""
    translation_units = compdb_parser.parse_commands(commands, the_config.files)
    return apply_checkers_for_translation_units(translation_units, the_config)


def apply_checkers_for_translation_units(translation_units, the_config):
    """For each tu apply the checkers and optionally the fixes"""
    all_violations = []
    for translation_unit in translation_units:
        all_violations += apply_checkers_for_translation_unit(translation_unit, the_config)

    if the_config.fix:
        apply_fixes_for_translation_unit(all_violations, the_config)

    return all_violations


def apply_checkers_for_translation_unit(translation_unit, the_config):
    """For each translation unit, apply the checkers"""
    # TODO Do not differentiation between tu and token based checker
    violations_per_tu = []
    if translation_unit:
        logging.info(colored("Applying checkers for '%s'", "magenta"), utils.only_filename(translation_unit.spelling))
        summary.get_summary().add_analyzed_translation_unit(translation_unit.spelling)

        # Apply the checkers
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


def apply_fixes_for_translation_unit(all_violations, the_config):
    """Apply the fixes"""
    for the_checker in config.ALL_FIXITS:
        logging.info(colored("Applying fixes for '%s'", "magenta"), the_checker.__module__)
        fixit.fix_violations(all_violations, the_checker)


def run(runner, the_config):
    compdb = compdb_parser.load_compdb(the_config.compdb)
    the_summary = summary.get_summary()
    if compdb:
        the_summary = runner(the_config, compdb)
    else:
        logging.error("Could not load compdb")
        sys.exit("Loading of compdb failed")
    return the_summary


def extract_checkers_from_string(checkers_string_list):
    active_checkers = []
    if not checkers_string_list:
        return config.ALL_CHECKERS
    for checker_string in checkers_string_list:
        for available_checker in config.ALL_CHECKERS:
            if checker_string.lower() in available_checker.__module__.lower():
                active_checkers.append(available_checker)
    return active_checkers


def parse_args():
    """Define and parse arguments"""
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
    parser.add_argument(
        "--checkers",
        nargs="+",
        help=(
            "List of checkers to be applied. Treated as substrings. Default: All checkers\n"
            "Example: '--checkers SAMO_TIDY_SUFFIX' would apply every checker which has 'SAMO_TIDY_SUFFIX' in its name"
        ),
        default=None,
    )
    parser.add_argument(
        "--fix", help="Apply fixes. Caution! This will change source files", action="store_true", default=False
    )
    parser.add_argument("--log_file", help="Full path to a log file", default=None)
    parser.add_argument(
        "--log_level", help="Log level. One of {DEBUG, INFO, WARN, ERROR, CRITICAL}. Default: INFO", default="info"
    )
    parser.add_argument(
        "--workers",
        help=f"Number of workers for parallel execution. Default: Number of CPUs which is {multiprocessing.cpu_count()}",
        type=int,
        metavar=f"[1-{multiprocessing.cpu_count()}]",
        choices=range(1, multiprocessing.cpu_count() + 1),
        default=multiprocessing.cpu_count(),
    )

    args = parser.parse_args()
    return args


def main(runner):
    """Entry point for serial and parallel runner"""
    args = parse_args()
    logger.setup_logger(args.log_level, args.log_file)

    active_checkers = extract_checkers_from_string(args.checkers)

    the_config = config.Config(
        active_checkers=active_checkers,
        compdb=args.compdb,
        files=args.files,
        log_level=args.log_level,
        workers=args.workers,
        fix=args.fix,
    )

    logging.critical(colored("CONFIG:\n" + pformat(the_config.present()), attrs=["dark"]))
    logging.critical(colored("Welcome. Lets run some static code analysis checks...", "magenta"))

    clang_setup.setup_clang()

    the_summary = run(runner, the_config)

    logging.critical(colored("SUMMARY:\n" + pformat(the_summary.present()), attrs=["dark"]))

    sys.exit(0)
