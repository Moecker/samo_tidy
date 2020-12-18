from clang import cindex

import samo_tidy.checker.checker as checker

ID = "TIDY_SAMO_SUFFIX_CASE"

# Checks whether an upper case "u" is provided for unsigned int literals
def token_based_rule(token):
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            for child_token in token.get_tokens():
                if "u" in child_token.spelling:
                    violation = checker.extract_violation(child_token, ID, "Lower Case suffix for unsigned integer")
    return violation


def fix(lines, violation):
    if violation.id != ID:
        return []
    violated_line = list(lines[violation.line])
    violated_line[violation.column] = violated_line[violation.column].upper()
    fixed_line = "".join(violated_line)
    lines[violation.line] = fixed_line
    return lines
