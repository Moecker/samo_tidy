from clang import cindex

import samo_tidy.checker.checker as checker


def rule(token):
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "int":
            violation = checker.extract_violation(token, "TIDY_SAMO_DUMMY", "DUMMY")
    return violation
