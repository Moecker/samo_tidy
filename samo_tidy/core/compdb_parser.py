import logging
import os
import traceback

import clang
from clang import cindex
from pprint import pformat

from samo_tidy.utils.utils import get_diagnostics_info


def load_compdb(directory):
    try:
        logging.info("Opening compilation database from directory '%s'", directory)
        compdb = cindex.CompilationDatabase.fromDirectory(directory)
        return compdb
    except cindex.CompilationDatabaseError as the_exception:
        logging.error(the_exception)
        logging.debug(the_exception, exc_info=True)
        return None


def parse_compdb(compdb):
    commands = compdb.getAllCompileCommands()
    logging.debug("Got %d command(s)", len(commands))
    translation_units = []
    for command in commands:
        logging.debug("Got file name %s", command.filename)
        logging.debug("Got arguments %s", list(command.arguments))
        translation_unit = create_translation_unit(command.filename, list(command.arguments))
        translation_units.append(translation_unit)
    return translation_units


def clean_args(args):
    to_remove_idx = []
    for idx, arg in enumerate(args):
        if arg.startswith("-c"):
            to_remove_idx.append(arg)
            to_remove_idx.append(args[idx + 1])
    for idx_to_remove in to_remove_idx:
        args.remove(idx_to_remove)
    return args


def debug_tokens(translation_unit):
    for token in translation_unit.cursor.walk_preorder():
        logging.debug("Token kind: %s", token.kind)


def create_translation_unit(source_file, args):
    index = cindex.Index.create()
    try:
        args = clean_args(args)
        logging.debug("Parsing %s with args %s", source_file, args)
        translation_unit = index.parse(source_file, args=args)
        logging.warning(get_diagnostics_info(translation_unit))
        return translation_unit
    except cindex.TranslationUnitLoadError as the_exception:
        logging.error(the_exception)
        logging.error("Current File was %s", source_file)
        logging.debug(the_exception, exc_info=True)
        return None
