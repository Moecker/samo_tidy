import logging
import platform
import os
import sys

from pprint import pformat
from clang import cindex


def only_filename(file_path):
    return os.path.basename(file_path)


def setup_clang():
    if platform.system() == "Linux":
        lib_location_file = "/usr/lib/llvm-10/lib/libclang-10.so"
        logging.info("Searching libclang file in '%s'", lib_location_file)
        cindex.Config.set_library_file(lib_location_file)
    elif platform.system() == "Darwin":
        lib_location_path = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
        logging.info("Searching libclang path in '%s'", lib_location_path)
        cindex.Config.set_library_path(lib_location_path)
    elif platform.system() == "Windows":
        sys.exit("Windows is not supported")
    else:
        sys.exit("Unknown OS")


def replace_if_none(to_be_checked, replacement_string, replacement_value=None):
    if to_be_checked:
        return to_be_checked
    else:
        return replacement_string


def log_diagnostics_info_summary(translation_unit):
    for d in translation_unit.diagnostics:
        if d.location.file:
            file_path = d.location.file.name
        else:
            file_path = "Unknown"

        log_function = logging.debug
        if d.severity > 2:
            log_function = logging.warning
        log_function(
            "Clang diagnostic: Severity '%s', Category '%s', Option '%s', Message: '%s', File '%s'",
            d.severity,
            replace_if_none(d.category_name, "Unknown Category"),
            replace_if_none(d.option, "Unknown Option"),
            d.spelling,
            only_filename(file_path),
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
