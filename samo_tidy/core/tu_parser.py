import logging

from clang import cindex

from samo_tidy.utils.utils import get_diagnostics_info, log_diagnostics_info_summary


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
    try:
        args = clean_args(args)
        logging.debug("Parsing %s with args %s", source_file, args)
        translation_unit = index.parse(source_file, args=args)
        logging.debug(get_diagnostics_info(translation_unit))
        log_diagnostics_info_summary(translation_unit)
        return translation_unit
    except cindex.TranslationUnitLoadError as the_exception:
        logging.error(the_exception)
        logging.error("Current File was %s", source_file)
        logging.debug(the_exception, exc_info=True)
        return None
