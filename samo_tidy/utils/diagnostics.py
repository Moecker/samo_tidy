from collections import defaultdict
from functools import partial
import logging

import samo_tidy.utils.utils as utils


def get_diag_info(diag):
    """Collection of important diag entries"""
    return {
        "severity": diag.severity,
        "location": diag.location,
        "spelling": diag.spelling,
        "category_name": diag.category_name,
        "option": diag.option,
    }


def get_diagnostics_by_severity(translation_unit):
    """Collect diag info as dict for tu name and severity"""
    diags_dict = defaultdict(partial(defaultdict, int))
    diags_dict[translation_unit.spelling] = get_diagnostics_by_severity_one_tu(translation_unit)
    return diags_dict


def get_diagnostics_by_severity_one_tu(translation_unit):
    """Collect diag info per severity"""
    diags_dict = defaultdict(int)
    for diagnostic in translation_unit.diagnostics:
        diags_dict[f"{diagnostic.severity}"] += 1
    return diags_dict


def get_diagnostics_info(translation_unit):
    """Pretty prints the diag info"""
    return pformat(("diags", [get_diag_info(d) for d in translation_unit.diagnostics]))


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
            f"{utils.only_filename(file_path)}:{diagnostic.location.line}:{diagnostic.location.column}",
        )


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
