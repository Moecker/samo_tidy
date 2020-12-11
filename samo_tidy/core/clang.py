import logging
import os

import clang
from clang import cindex

clang.cindex.Config.set_library_file("/usr/local/opt/llvm/lib/libclang.dylib")


def load_compilation_db(directory):
    try:
        logging.info("Opening compilation database from directory '%s'", directory)
        compdb = clang.cindex.CompilationDatabase.fromDirectory(directory)
        return compdb
    except clang.cindex.CompilationDatabaseError as the_exception:
        logging.error(the_exception)
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
        print(dir(translation_unit))
    return translation_units


def create_translation_unit(source_file, args):
    index = cindex.Index.create()
    translation_unit = index.parse(source_file, args=args)
    for token in translation_unit.cursor.walk_preorder():
        logging.debug("Token kind: %s", token.kind)
    return translation_unit
