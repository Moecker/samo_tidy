from clang import cindex

import samo_tidy.checker.checker as checker

ID = "TIDY_SAMO_UNSIGNED_INT"


def token_based_rule(token):
    """Dummy Check"""
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            violation = checker.extract_violation(token, ID, "Usage of unsigned int")
    return violation
