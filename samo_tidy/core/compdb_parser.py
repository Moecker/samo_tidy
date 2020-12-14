import logging
import os
import sys
import time


from clang import cindex

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.utils.utils as utils


def load_compdb(directory):
    try:
        logging.info("Opening compilation database from directory '%s'", directory)
        compdb = cindex.CompilationDatabase.fromDirectory(directory)
        return compdb
    except cindex.CompilationDatabaseError as the_exception:
        logging.error(the_exception)
        logging.debug(the_exception, exc_info=True)
        return None


def parse_single_command(command):
    logging.info("Parsing file '%s'", command.filename)
    logging.debug("Using file name '%s'", utils.only_filename(command.filename))
    logging.debug("Using directory '%s'", command.directory)
    logging.debug("Using arguments '%s'", list(command.arguments))
    translation_unit = tu_parser.create_translation_unit(
        os.path.join(command.directory, command.filename), list(command.arguments), command.directory
    )
    return translation_unit


def computation(args):
    start, end, the_list = args
    ret = []

    for i in range(start, end):
        ret.append(the_list[i] * 100)
        time.sleep(0.1)
    return ret


def parse_from_commands(args):
    start, end, commands = args
    translation_units = []

    for i in range(start, end):
        translation_unit = parse_single_command(command)
        translation_units.append(translation_unit)
    return translation_units


def parse_compdb(compdb, list_of_files=None):
    commands = compdb.getAllCompileCommands()
    if not commands:
        err_msg = "Compilation Database invalid"
        logging.error(err_msg)
        sys.exit(err_msg)

    logging.info("Found %d command(s) in compilation database", len(commands))

    translation_units = []
    number_of_skipped_files = 0

    # TODO Does not work: ValueError: ctypes objects containing pointers cannot be pickled
    # output = utils.parallel(commands, 4, parse_from_commands)

    for command in commands:
        # Check if we want to parse the translation unit based on the file name pattern
        if list_of_files and not any(word in command.filename for word in list_of_files):
            continue
        if any(word in command.filename for word in ["external/"]):
            logging.debug("Skipping external file '%s'", command.filename)
            number_of_skipped_files += 1
            continue

        translation_unit = parse_single_command(command)
        translation_units.append(translation_unit)

    if number_of_skipped_files > 0:
        logging.info("Skipped %d file(s)", number_of_skipped_files)
    return translation_units


def clean_args(args):
    # Some arguments cause problems - remove them
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
