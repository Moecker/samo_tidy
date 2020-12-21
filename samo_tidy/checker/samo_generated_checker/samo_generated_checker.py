from clang import cindex

import samo_tidy.checker.checker as checker

ID = "SAMO_GENERATED_CHECKER"
MSG = "Violation of SAMO_GENERATED_CHECKER"


def token_based_rule(token):
    violation = None
    violation = checker.extract_violation(token, ID, f"{MSG} for {token.spelling}")
    return violation


def translation_unit_based_rule(translation_unit):
    violations = []
    for token in translation_unit.cursor.walk_preorder():
        violation = checker.extract_violation(token, ID, f"{MSG} for {translation_unit.spelling}")
        if violation:
            violations.append(violation)
    return violations


def fix(lines, violation):
    if violation.id != ID:
        return []
    return lines
