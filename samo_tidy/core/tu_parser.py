import logging
import os

from clang import cindex

import samo_tidy.utils.utils as utils

DEFAULT_ACTIVE_ARGUMENTS = ["-Weverything"]
DEFAULT_IGNORED_ARGUMENTS = [
    "-Wno-unused-command-line-argument",
    "-Wno-c++98-compat",
    "-Wno-c++98-compat-pedantic",
    "-Wno-documentation",
]
DEFAULT_ARGUMENTS = DEFAULT_ACTIVE_ARGUMENTS + DEFAULT_IGNORED_ARGUMENTS


def clean_args(args):
    to_be_removed_argx = []
    for idx, arg in enumerate(args):
        if arg.startswith("-c"):
            to_be_removed_argx.append(arg)
            to_be_removed_argx.append(args[idx + 1])
    for idx_to_remove in to_be_removed_argx:
        args.remove(idx_to_remove)
    return args


def absolute_path_include(args, directory):
    if directory:
        to_be_changed_indexes = []
        for idx, arg in enumerate(args):
            if arg.startswith("-I") or arg.startswith("-isystem"):
                if not args[idx + 1].startswith("/"):
                    to_be_changed_indexes.append(idx + 1)
        for to_be_changed_index in to_be_changed_indexes:
            args[to_be_changed_index] = os.path.join(directory, args[to_be_changed_index])
    return args


def create_translation_unit(source_file, args=[], directory=None):
    index = cindex.Index.create()
    args = DEFAULT_ARGUMENTS + args
    try:
        # Core part: parse the source file using clang
        args = clean_args(args)
        args = absolute_path_include(args, directory)
        logging.debug("Parsing '%s' with args '%s'", utils.only_filename(source_file), args)
        translation_unit = index.parse(source_file, args=args)
        utils.log_diagnostics_info_summary(translation_unit)
        return translation_unit
    except cindex.TranslationUnitLoadError as the_exception:
        logging.error(the_exception)
        logging.error("Failed to parse '%s'", utils.only_filename(source_file))
        logging.debug(the_exception, exc_info=True)
        return None
