from clang import cindex

import samo_tidy.checker.checker as checker

# Checks for multiple classes in one translation unit
def translation_unit_based_rule(translation_unit):
    # TODO Make this generic and use also in nested namespaces
    violations = []
    classes = []

    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.CLASS_DECL:
            if token.is_definition:
                if token.location.file.name == translation_unit.spelling:
                    classes.append(token.spelling)

    # TODO Output all classes as violations
    if len(classes) > 1:
        violation = checker.extract_violation(
            token,
            "TIDY_SAMO_MULTIPLE_CLASSES",
            f"Multiple {len(classes)} classes in one translation unit",
        )
        if violation:
            violations.append(violation)
    return violations
