import logging

from clang import cindex

import samo_tidy.utils.utils as utils

DEFAULT_ACTIVE_ARGUMENTS = ["-std=c++14", "-Weverything"]
DEFAULT_IGNORED_ARGUMENTS = ["-Wno-unused-command-line-argument"]
DEFAULT_ARGUMENTS = DEFAULT_ACTIVE_ARGUMENTS + DEFAULT_IGNORED_ARGUMENTS


def clean_args(args):
    to_remove_idx = []
    for idx, arg in enumerate(args):
        if arg.startswith("-c"):
            to_remove_idx.append(arg)
            to_remove_idx.append(args[idx + 1])
    for idx_to_remove in to_remove_idx:
        args.remove(idx_to_remove)
    return args


def create_translation_unit(source_file, args=[]):
    index = cindex.Index.create()
    args = DEFAULT_ARGUMENTS + args
    try:
        args = clean_args(args)
        logging.debug("Parsing '%s' with args '%s'", utils.only_filename(source_file), args)
        translation_unit = index.parse(source_file, args=args)
        # TODO Too noisy, add a "verbose" log level
        # logging.debug(utils.get_diagnostics_info(translation_unit))
        utils.log_diagnostics_info_summary(translation_unit)
        return translation_unit
    except cindex.TranslationUnitLoadError as the_exception:
        logging.error(the_exception)
        logging.error("Failed to parse '%s'", utils.only_filename(source_file))
        logging.debug(the_exception, exc_info=True)
        return None
