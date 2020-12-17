from pprint import pformat
from termcolor import colored
import logging
import os
import sys


def make_link(text):
    return colored(f"file://{text}", attrs=["underline"])


def is_commented_line(line):
    return line.startswith("//")


def only_filename(file_path):
    return os.path.basename(file_path)


def get_ignored_file_strings():
    return ["/usr/", "/lib/gcc/", "external"]


def shall_ignore_based_on_file_name(file_name):
    return any(word in file_name for word in get_ignored_file_strings())


def replace_if_none(to_be_checked, replacement_string, replacement_value=None):
    if to_be_checked:
        return to_be_checked
    else:
        return replacement_string


def shall_exclude_diagnostic_message(message):
    exclusion_list = [
        "-fno-canonical-system-headers",
        "-Wunused-but-set-parameter",
        "-Wno-free-nonheap-object",
        "-Werror=init-list-lifetime",
        "-Werror=class-conversion",
    ]
    return any(word in message for word in exclusion_list)


def log_diagnostics_info_summary(translation_unit):
    # TODO logging.debug(get_diagnostics_info(translation_unit))
    for diagnostic in translation_unit.diagnostics:
        if shall_exclude_diagnostic_message(diagnostic.spelling):
            continue

        if diagnostic.location.file:
            file_path = diagnostic.location.file.name
        else:
            file_path = "Unknown"

        log_function = logging.debug
        if diagnostic.severity > 3:
            log_function = logging.warning

        log_function(
            "Clang diagnostic: Severity '%s', Message: '%s', File '%s'",
            diagnostic.severity,
            diagnostic.spelling,
            f"{only_filename(file_path)}:{diagnostic.location.line}:{diagnostic.location.column}",
        )


def get_diagnostics_info(translation_unit):
    return pformat(("diags", [get_diag_info(d) for d in translation_unit.diagnostics]))


def get_diag_info(diag):
    return {
        "severity": diag.severity,
        "location": diag.location,
        "spelling": diag.spelling,
        "category_name": diag.category_name,
        "option": diag.option,
    }


def join_and_strip_file_content(lines):
    return " ".join([x.strip() for x in lines])


def debug_file_content(file_path):
    with open(file_path) as f:
        logging.debug(
            "File '%s' looks like: '%s'", only_filename(file_path), join_and_strip_file_content(f.readlines())
        )
