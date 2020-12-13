import logging
import os

from clang import cindex

import samo_tidy.core.tu_parser as tu_parser


def load_compdb(directory):
    try:
        logging.info("Opening compilation database from directory '%s'", directory)
        compdb = cindex.CompilationDatabase.fromDirectory(directory)
        return compdb
    except cindex.CompilationDatabaseError as the_exception:
        logging.error(the_exception)
        logging.debug(the_exception, exc_info=True)
        return None


def parse_compdb(compdb, list_of_file=None):
    commands = compdb.getAllCompileCommands()
    logging.debug("Got %d command(s)", len(commands))
    translation_units = []
    no_of_skipped_files = 0
    for command in commands:
        if list_of_file and not any(word in command.filename for word in list_of_file):
            continue
        if "external/" in command.filename:
            logging.debug("Skipping: '%s'", command.filename)
            no_of_skipped_files += 1
            continue
        logging.info("Analyzing: '%s'", command.filename)
        logging.debug("Got file name '%s'", command.filename)
        logging.debug("Got directory '%s'", command.directory)
        logging.debug("Got arguments '%s'", list(command.arguments))
        translation_unit = tu_parser.create_translation_unit(
            os.path.join(command.directory, command.filename), list(command.arguments)
        )
        translation_units.append(translation_unit)
    if no_of_skipped_files > 0:
        logging.info("Skipped %d file(s)", no_of_skipped_files)
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
        logging.debug("Token kind: '%s'", token.kind)
