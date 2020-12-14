from clang import cindex

import samo_tidy.checker.checker as checker


def rule(token):
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            violation = checker.extract_violation(token, "TIDY_SAMO_UNSIGNED_INT", "Using unsigned int")
    return violation
