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


def fix(lines, violation):
    """Apply fix for lower case 'u'"""
    if violation.id != ID:
        return []
    true_index = violation.line - 1
    violated_line = list(lines[true_index])
    logging.info(f"Fixing {violation}")
    violated_line[violation.column] = violated_line[violation.column].upper()
    fixed_line = "".join(violated_line)
    lines[true_index] = fixed_line
    return lines
