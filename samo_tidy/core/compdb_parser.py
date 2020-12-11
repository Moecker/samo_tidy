import logging
import os
import traceback

import clang
from clang import cindex

cindex.Config.set_library_file("/usr/local/opt/llvm/lib/libclang.dylib")


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
        translation_unit = create_translation_unit(
            command.filename, list(command.arguments)
        )
        translation_units.append(translation_unit)
    return translation_units


def create_translation_unit(source_file, args):
    index = cindex.Index.create()
    try:
        translation_unit = index.parse(source_file, args=args)
        for token in translation_unit.cursor.walk_preorder():
            logging.debug("Token kind: %s", token.kind)
        return translation_unit
    except cindex.TranslationUnitLoadError as the_exception:
        logging.error(the_exception)
        logging.error("Current File was %s", source_file)
        logging.debug(the_exception, exc_info=True)
        return None
