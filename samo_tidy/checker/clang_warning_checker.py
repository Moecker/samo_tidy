import logging

import samo_tidy.checker.checker as checker
import samo_tidy.utils.utils as utils

# Interprets clang diagnostics warnings (aka compiler warnings) as violations
def check_for_clang_warnings(translation_unit):
    violations = []
    logging.info(
        "Analyzing translation unit '%s' with checker '%s'",
        utils.only_filename(translation_unit.spelling),
        __name__,
    )
    for diagnostic in translation_unit.diagnostics:
        if diagnostic.option and diagnostic.location.file:
            if diagnostic.option.startswith("-W"):
                the_id = "TIDY_CLANG_" + diagnostic.option[2:].upper().replace("-", "_")
                violation = checker.extract_violation(diagnostic, the_id, diagnostic.spelling)
            violations.append(violation)
    return violations
