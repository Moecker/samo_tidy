from clang import cindex

import samo_tidy.checker.checker as checker

# Just a dummy check
def token_based_rule(token):
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            violation = checker.extract_violation(token, "TIDY_SAMO_UNSIGNED_INT", "Usage of unsigned int")
    return violation
