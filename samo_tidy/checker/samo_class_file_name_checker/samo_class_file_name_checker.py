from clang import cindex
import re
from os.path import splitext, basename


import samo_tidy.checker.checker as checker

ID = "SAMO_CLASS_FILE_NAME_CHECKER"
MSG = "Violation of SAMO_CLASS_FILE_NAME_CHECKER"


def token_based_rule(token):
    violation = None
    violation = checker.extract_violation(token, ID, f"{MSG} for {token.spelling}")
    return violation


def translation_unit_based_rule(translation_unit):
    violations = []
    first_class = None
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.CLASS_DECL:
            if token.is_definition():
                if token.location.file.name == translation_unit.spelling:
                    first_class = token
                    break

    if first_class:
        computed_name, basename = compute_expected_name(first_class, translation_unit.spelling)
        if computed_name != basename:
            violation = checker.extract_violation(token, ID, f"{MSG} for {translation_unit.spelling}")
            if violation:
                violations.append(violation)
    return violations


def fix(lines, violation):
    if violation.id != ID:
        return []
    return lines


def translation_unit_basename_and_extension(translation_unit_name):
    filename, extension = splitext(translation_unit_name)
    bname = basename(translation_unit_name)
    return bname, extension


def compute_expected_name(first_class, translation_unit_name):
    basename, extension = translation_unit_basename_and_extension(translation_unit_name)
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    computed_name = pattern.sub("_", first_class.spelling).lower()
    computed_name += extension
    return computed_name, basename
