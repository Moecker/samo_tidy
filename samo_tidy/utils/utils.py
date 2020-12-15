import logging
import platform
import os
import sys
import multiprocessing
import itertools

from pprint import pformat
from clang import cindex


def only_filename(file_path):
    return os.path.basename(file_path)


def get_ignored_file_strings():
    return ["/usr/", "/lib/gcc/", "external"]


def shall_ignore_based_on_file_name(file_name):
    return any(word in file_name for word in get_ignored_file_strings())


def setup_clang():
    # The cindex.Config class is of global state.
    # TODO When executing test in parallel - for instance - we run into problems.
    cindex.Config.loaded = False
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


def parallel(the_list, workers, the_function):
    list_length = len(the_list)
    if list_length == 0:
        return []

    workers = min(workers, list_length)
    batch = int(list_length / workers)

    output = []
    with multiprocessing.Pool(workers) as pool:
        output = pool.map(
            the_function,
            [
                (start, min(start + batch, list_length), the_list)
                for start in range(
                    0,
                    list_length,
                    batch,
                )
            ],
        )
    return list(itertools.chain.from_iterable(output))
