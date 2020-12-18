from clang import cindex

import samo_tidy.checker.checker as checker

# Checks whether an upper case "u" is provided for unsigned int literals
def token_based_rule(token):
    violation = None
    if token.kind == cindex.CursorKind.INTEGER_LITERAL:
        if token.type.spelling == "unsigned int":
            for child_token in token.get_tokens():
                if "u" in child_token.spelling:
                    violation = checker.extract_violation(
                        child_token, "TIDY_SAMO_SUFFIX_CASE", "Lower Case suffix for unsigned integer"
                    )
    return violation


def fixit(violation):
    lines = []
    with open(violation.file_path) as the_file:
        lines = the_file.readlines()

    violated_line = list(lines[violation.line])
    violated_line[violation.column] = violated_line[violation.column].upper()
    fixed_line = "".join(violated_line)

    lines[violation.line] = fixed_line

    with open(violation.file_path, "w") as the_file:
        the_file.writelines(lines)
