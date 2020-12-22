from clang import cindex
import re
from os.path import splitext, basename

import samo_tidy.checker.checker as checker

ID = "SAMO_CLASS_NAME_CHECKER"
MSG = "File name should be named as the class it contains"


def translation_unit_based_rule(translation_unit):
    violations = []
    classes = []
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.CLASS_DECL:
            if token.is_definition():
                if token.location.file.name == translation_unit.spelling:
                    classes.append(token)

    for the_class in classes:
        computed_name, basename = compute_expected_name(the_class, translation_unit.spelling)
        if computed_name != basename:
            violation = checker.extract_violation(
                the_class,
                ID,
                f"File name should be named '{computed_name}' as derived from the class '{the_class.spelling}'",
            )
            if violation:
                violations.append(violation)
    return violations


def fix(lines, violation):
    # TODO Either rename the file or the class. This is hardly automatable w/o side effects
    return lines


def translation_unit_basename_and_extension(translation_unit_name):
    filename, extension = splitext(translation_unit_name)
    the_basename = basename(translation_unit_name)
    return the_basename, extension


def compute_expected_name(first_class, translation_unit_name):
    the_basename, extension = translation_unit_basename_and_extension(translation_unit_name)
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    computed_name = pattern.sub("_", first_class.spelling).lower()
    computed_name += extension
    return computed_name, the_basename
