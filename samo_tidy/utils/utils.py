from pprint import pformat
from termcolor import colored
import logging
import os
import sys


def make_link(text):
    """Beautify and clickable links"""
    return colored(f"file://{text}", attrs=["underline"])


def is_commented_line(line):
    """Naive check for commented lines"""
    return line.startswith("//")


def only_filename(file_path):
    """Return the filename, stripping its absolute part"""
    return os.path.basename(file_path)


def get_ignored_file_strings():
    """A list of known to be ignored file path substrings"""
    return ["/usr/", "/lib/gcc/", "external"]


def shall_ignore_based_on_file_name(file_name):
    """True if the filename contains a word of the forbidden list"""
    return any(word in file_name for word in get_ignored_file_strings())


def replace_if_none(to_be_checked, replacement_string):
    """Return a replacement is to be checked is empty (None or empty string)"""
    if to_be_checked:
        return to_be_checked
    else:
        return replacement_string


def shall_exclude_diagnostic_message(message):
    """Exclude certain diagnostics messages"""
    exclusion_list = [
        "-fno-canonical-system-headers",
        "-Wunused-but-set-parameter",
        "-Wno-free-nonheap-object",
        "-Werror=init-list-lifetime",
        "-Werror=class-conversion",
    ]
    return any(word in message for word in exclusion_list)


def log_diagnostics_info_summary(translation_unit):
    """Logs a oneliner per diagnostics entry of the translation unit"""
    for diagnostic in translation_unit.diagnostics:
        if shall_exclude_diagnostic_message(diagnostic.spelling):
            continue

        if diagnostic.location.file:
            file_path = diagnostic.location.file.name
        else:
            file_path = "Unknown"

        log_function = logging.debug
        if diagnostic.severity > 2:
            log_function = logging.warning

        log_function(
            "Clang diagnostic: Severity '%s', Message: '%s', File '%s'",
            diagnostic.severity,
            diagnostic.spelling,
            f"{only_filename(file_path)}:{diagnostic.location.line}:{diagnostic.location.column}",
        )


def get_diagnostics_info(translation_unit):
    """Pretty prints the diag info"""
    return pformat(("diags", [get_diag_info(d) for d in translation_unit.diagnostics]))


def get_diag_info(diag):
    """Collection of important diag entries"""
    return {
        "severity": diag.severity,
        "location": diag.location,
        "spelling": diag.spelling,
        "category_name": diag.category_name,
        "option": diag.option,
    }


def join_and_strip_file_content(lines):
    """Strips every entry of lines and combines it again"""
    return " ".join([x.strip() for x in lines])


def debug_file_content(file_path):
    """Simple output of file"""
    with open(file_path) as f:
        logging.debug(
            "File '%s' looks like: '%s'", only_filename(file_path), join_and_strip_file_content(f.readlines())
        )
