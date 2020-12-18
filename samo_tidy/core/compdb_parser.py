from clang import cindex
from termcolor import colored
import logging
import os
import sys

import samo_tidy.core.summary as summary
import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.utils.utils as utils


def load_compdb(directory):
    try:
        logging.info(
            colored("Opening compilation database '%s'", "green"),
            utils.make_link(os.path.join(directory, "compile_commands.json")),
        )
        compdb = cindex.CompilationDatabase.fromDirectory(directory)
        return compdb
    except cindex.CompilationDatabaseError as the_exception:
        logging.error(the_exception)
        logging.debug(the_exception, exc_info=True)
        return None


def parse_single_command(command):
    absolute_file_name = os.path.join(command.directory, command.filename)
    logging.info(
        colored("Parsing file '%s'", "green"),
        utils.make_link(absolute_file_name),
    )
    logging.debug("Using file name (not absolute path) '%s'", utils.only_filename(command.filename))
    logging.debug("Using directory '%s'", command.directory)
    logging.debug("Using arguments '%s'", list(command.arguments))
    translation_unit = tu_parser.create_translation_unit(absolute_file_name, list(command.arguments), command.directory)
    return translation_unit


def parse_compdb(compdb):
    commands = compdb.getAllCompileCommands()
    if not commands:
        err_msg = "Compilation Database invalid"
        logging.error(err_msg)
        sys.exit(err_msg)

    logging.info(colored("Found %d command(s) in compilation database", attrs=["dark"]), len(commands))
    return commands


def parse_commands(commands, list_of_files=None):
    translation_units = []
    number_of_skipped_files = 0

    for command in commands:
        # Check if we want to parse the translation unit based on the file name pattern
        if list_of_files and not any(word in command.filename for word in list_of_files):
            summary.get_summary().add_skipped_commands(command.filename)
            continue
        if utils.shall_ignore_based_on_file_name(command.filename):
            logging.debug("Skipping external file '%s'", command.filename)
            number_of_skipped_files += 1
            summary.get_summary().add_skipped_filename(command.filename)
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
