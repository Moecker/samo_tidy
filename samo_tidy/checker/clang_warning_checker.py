import logging
from termcolor import colored

import samo_tidy.checker.checker as checker
import samo_tidy.utils.utils as utils

ID_PREFIX = "TIDY_CLANG_"


def check_for_clang_warnings(translation_unit):
    """Interprets clang diagnostics warnings (aka compiler warnings) as violations
    The checker differs from the other ones as it operates on the translation unit directly
    """
    violations = []
    logging.info(
        colored("Analyzing translation unit '%s' with checker '%s'", "cyan"),
        utils.only_filename(translation_unit.spelling),
        __name__,
    )

    for diagnostic in translation_unit.diagnostics:
        if diagnostic.option and diagnostic.location.file:
            if diagnostic.option.startswith("-W"):
                the_id = ID_PREFIX + diagnostic.option[2:].upper().replace("-", "_")
                violation = checker.extract_violation(diagnostic, the_id, diagnostic.spelling)
            violations.append(violation)
    return violations
