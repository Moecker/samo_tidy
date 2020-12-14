from clang import cindex

import samo_tidy.checker.checker as checker

# Checks whether an upper case "u" is provided for unsigned int literals
def token_based_rule(token):
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            for child_token in token.get_tokens():
                if "u" in child_token.spelling:
                    violation = checker.extract_violation(child_token, "TIDY_SAMO_SUFFIX_CASE", "Lower Case suffix")
    return violation
