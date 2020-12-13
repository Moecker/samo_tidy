import logging
import platform
import os
import sys

from pprint import pformat
from clang import cindex


def setup_clang():
    if platform.system() == "Linux":
        lib_location_file = "/usr/lib/llvm-10/lib/libclang-10.so"
        logging.info("Searching libclang file in '%s'", lib_location_file)
        cindex.Config.set_library_file(lib_location_file)
    if platform.system() == "Darwin":
        lib_location_path = "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
        logging.info("Searching libclang path in '%s'", lib_location_path)
        cindex.Config.set_library_path(lib_location_path)
    if platform.system() == "Windows":
        sys.exit("Windows is not supported")


def log_diagnostics_info_summary(translation_unit):
    for d in translation_unit.diagnostics:
        logging.warning(
            "Clang diagnostic of category '%s' from option '%s' with message: '%s' in file '%s'",
            d.category_name,
            d.option,
            d.spelling,
            d.location.file,
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


def debug_file_content(file_path):
    with open(file_path) as f:
        logging.debug("File '%s' looks like: '%s'", file_path, pformat("".join(f.readlines())))
