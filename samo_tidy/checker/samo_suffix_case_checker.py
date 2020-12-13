from clang import cindex

import samo_tidy.checker.checker as checker


def rule(token):
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            for child_token in token.get_tokens():
                violation = None
                if "u" in child_token.spelling:
                    violation = checker.extract_violation(child_token, "TIDY_SAMO_SUFFIX_CASE", "Lower Case suffix")
                if not "u" in child_token.spelling.lower():
                    violation = checker.extract_violation(child_token, "TIDY_SAMO_SUFFIX_MISSING", "Suffix missing")
    return violation
