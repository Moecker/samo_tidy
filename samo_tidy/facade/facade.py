import argparse
import logging
import sys

from samo_tidy.core.compdb_parser import load_compdb, parse_compdb
from samo_tidy.checker.checker import check_for_ints
from samo_tidy.utils.utils import setup_clang


def apply_checkers_for_translation_units(translation_units):
    for tu in translation_units:
        if tu:
            check_for_ints(tu)
        else:
            logging.warning("Skipping translation unit")


def run(compdb_root_dir, files=None):
    compdb = load_compdb(compdb_root_dir)
    if compdb:
        translation_units = parse_compdb(compdb)
    else:
        logging.error("Could not load compdb")
        sys.exit("Loading of compdb failed")
    apply_checkers_for_translation_units(translation_units)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compdb", required=True, help="Directory which contains the 'compile_comands.json' file")
    parser.add_argument("--files", nargs="+", help="List of file from compdb to be analysed")
    parser.add_argument("--verbose", action="store_true", help="Produces more debug output")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    setup_clang()
    run(args.compdb, args.files)


if __name__ == "__main__":
    main()
