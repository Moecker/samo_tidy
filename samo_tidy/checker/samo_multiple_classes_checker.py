from clang import cindex

import samo_tidy.checker.checker as checker

ID = "TIDY_SAMO_MULTIPLE_CLASSES"
ALLOWED_NUMBER_OF_CLASSES_PER_FILE = 1


def translation_unit_based_rule(translation_unit):
    """Checks for multiple classes in one translation unit"""
    violations = []
    classes = []

    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.CLASS_DECL:
            if token.is_definition:
                if token.location.file.name == translation_unit.spelling:
                    classes.append(token.spelling)

    if len(classes) > ALLOWED_NUMBER_OF_CLASSES_PER_FILE:
        for the_class in classes:
            violation = checker.extract_violation(
                token,
                ID,
                f"Multiple of {len(classes)} classes '{the_class}' in one translation unit",
            )
            if violation:
                violations.append(violation)
    return violations
