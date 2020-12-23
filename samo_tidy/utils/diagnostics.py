from collections import defaultdict
from functools import partial


def get_diagnostics_by_severity(translation_unit):
    diags_dict = defaultdict(partial(defaultdict, int))
    diags_dict[translation_unit.spelling] = get_diagnostics_by_severity_one_tu(translation_unit)
    return diags_dict


def get_diagnostics_by_severity_one_tu(translation_unit):
    diags_dict = defaultdict(int)
    for diagnostic in translation_unit.diagnostics:
        diags_dict[f"{diagnostic.severity}"] += 1
    return diags_dict
