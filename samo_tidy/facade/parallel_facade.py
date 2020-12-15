import logging
import sys

import samo_tidy.core.compdb_parser as compdb_parser

import samo_tidy.facade.facade as facade


def run_parallel(compdb_root_dir, files=None):
    compdb = compdb_parser.load_compdb(compdb_root_dir)
    translation_units = compdb_parser.parse_compdb(compdb, files)
    facade.apply_checkers_for_translation_units(translation_units)
