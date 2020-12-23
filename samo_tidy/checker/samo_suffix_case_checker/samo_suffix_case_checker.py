from clang import cindex
import logging

import samo_tidy.checker.checker as checker

ID = "TIDY_SAMO_SUFFIX_CASE"


def token_based_rule(token):
    """Checks whether an upper case "u" is provided for unsigned int literals"""
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            for child_token in token.get_tokens():
                if "u" in child_token.spelling:
                    violation = checker.extract_violation(child_token, ID, "Lower Case suffix for unsigned integer")
    return violation


def fix_rule(violated_line, violation):
    fixed_line = violated_line
    fixed_line[violation.column] = violated_line[violation.column].upper()
    return fixed_line
