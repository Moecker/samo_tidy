from clang import cindex
import logging
import os

import samo_tidy.core.summary as summary
import samo_tidy.utils.diagnostics as diagnostics
import samo_tidy.utils.utils as utils

DEFAULT_ACTIVE_ARGUMENTS = ["--std=c++14", "-Weverything"]
DEFAULT_IGNORED_ARGUMENTS = [
    "-Wno-unused-command-line-argument",
    "-Wno-c++98-compat",
    "-Wno-c++98-compat-pedantic",
    "-Wno-documentation",
]
DEFAULT_ARGUMENTS = DEFAULT_ACTIVE_ARGUMENTS + DEFAULT_IGNORED_ARGUMENTS


def clean_args(args):
    """Cleans arguments from compdb.
    Some arguments cause problems - remove them"""
    to_remove_idx = []
    for idx, arg in enumerate(args):
        if arg.startswith("-c"):
            to_remove_idx.append(arg)
            to_remove_idx.append(args[idx + 1])
    for idx_to_remove in to_remove_idx:
        args.remove(idx_to_remove)
    return args


def absolute_path_include(args, directory):
    """Changes the relative include directory an absolute path from compdb directory info"""
    if directory:
        to_be_changed_indexes = []
        for idx, arg in enumerate(args):
            if arg.startswith("-I") or arg.startswith("-isystem"):
                # Only consider relative paths
                if not args[idx + 1].startswith("/"):
                    to_be_changed_indexes.append(idx + 1)
        for to_be_changed_index in to_be_changed_indexes:
            args[to_be_changed_index] = os.path.join(directory, args[to_be_changed_index])
    return args


def create_translation_unit(source_file, args=[], directory=None):
    """Use clang parser to parse the source file with given args.
    Returns the translation unit on success, None on failure"""
    index = cindex.Index.create()
    args = DEFAULT_ARGUMENTS + args
    try:
        args = clean_args(args)
        args = absolute_path_include(args, directory)
        logging.debug("Parsing '%s' with args '%s'", utils.only_filename(source_file), args)
        translation_unit = index.parse(source_file, args=args)
        diagnostics.log_diagnostics_info_summary(translation_unit)
        return translation_unit
    except cindex.TranslationUnitLoadError as the_exception:
        logging.error(the_exception)
        logging.error("Failed to parse '%s'", utils.only_filename(source_file))
        logging.debug(the_exception, exc_info=True)
        summary.get_summary().add_failed_translation_units(source_file)
        return None
