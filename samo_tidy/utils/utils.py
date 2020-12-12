import logging
from pprint import pformat
import clang
from clang import cindex
import os


def setup_clang():
    # LINUX
    cindex.Config.set_library_path("/usr/local/opt/llvm/lib")
    # MAC
    cindex.Config.set_library_path(
        "/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib"
    )


def get_diagnostics_info(translation_unit):
    return pformat(("diags", [get_diag_info(d) for d in translation_unit.diagnostics]))


def get_diag_info(diag):
    return {
        "severity": diag.severity,
        "location": diag.location,
        "spelling": diag.spelling,
        "ranges": diag.ranges,
        "fixits": diag.fixits,
    }


def debug_file_content(file_path):
    with open(file_path) as f:
        logging.debug("File %s looks like: %s", file_path, pformat(f.readlines()))
