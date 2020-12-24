from termcolor import colored
import logging
import os
import sys


def debug_file_content(file_path):
    """Simple output of file"""
    with open(file_path) as f:
        logging.debug(
            "File '%s' looks like: '%s'", only_filename(file_path), join_and_strip_file_content(f.readlines())
        )


def get_ignored_file_strings():
    """A list of known to be ignored file path substrings"""
    return ["/usr/", "/lib/gcc/", "external"]


def is_commented_line(line):
    """Naive check for commented lines"""
    return line.startswith("//")


def join_and_strip_file_content(lines):
    """Strips every entry of lines and combines it again"""
    return " ".join([x.strip() for x in lines])


def make_link(text):
    """Beautify and clickable links"""
    return colored(f"file://{text}", attrs=["underline"])


def only_filename(file_path):
    """Return the filename, stripping its absolute part"""
    return os.path.basename(file_path)


def replace_if_none(to_be_checked, replacement_string):
    """Return a replacement is to be checked is empty (None or empty string)"""
    if to_be_checked:
        return to_be_checked
    else:
        return replacement_string


def shall_ignore_based_on_file_name(file_name):
    """True if the filename contains a word of the forbidden list"""
    return any(word in file_name for word in get_ignored_file_strings())
