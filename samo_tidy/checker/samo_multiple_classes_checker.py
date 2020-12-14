from clang import cindex

import samo_tidy.checker.checker as checker
import samo_tidy.utils.utils as utils

# Checks for multiple classes in one translation unit
def translation_unit_based_rule(translation_unit):
    violations = []
    classes = []

    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.CLASS_DECL:
            classes.append(token.spelling)

    if len(classes) > 1:
        violation = checker.extract_violation(
            token,
            "TIDY_SAMO_MULTIPLE_CLASSES",
            f"Using multiple <{len(classes)}> classes in one translation unit <{utils.only_filename(translation_unit.spelling)}>",
        )
        if violation:
            violations.append(violation)
    return violations
