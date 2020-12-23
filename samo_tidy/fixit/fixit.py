import logging


# TODO Deprecated in favor of fix_violations_lines
def fix_violations(violations, fix_function):
    """Applies a fix function for every violaton in a list"""
    for violation in violations:
        fix_violation(violation, fix_function)


# TODO Deprecated in favor of fix_violation_line
def fix_violation(violation, fix_function):
    """Apply fix function for given violation, expects a line-violation"""
    lines = []
    with open(violation.file_path) as the_file:
        lines = the_file.readlines()

    fixed_lines = fix_function(lines, violation)

    if fixed_lines:
        with open(violation.file_path, "w") as the_file:
            the_file.writelines(fixed_lines)
    return fixed_lines


def fix_violations_lines(violations, fix_function):
    """Applies a fix function for every violaton in a list"""
    for violation in violations:
        fix_violation_line(violation, fix_function)


def fix_violation_line(violation, fix_function):
    """Apply fix function for given violation, expects a line-violation"""
    lines = []
    with open(violation.file_path) as the_file:
        lines = the_file.readlines()

    fixed_lines = fix_per_line(lines, violation, fix_function)

    if fixed_lines:
        with open(violation.file_path, "w") as the_file:
            the_file.writelines(fixed_lines)
    return fixed_lines


def fix_per_line(lines, violation, fix_function):
    """Apply fix function for lines"""
    true_index = violation.line - 1
    violated_line = list(lines[true_index])
    logging.info(f"Fixing {violation}")

    fixed_line_list = fix_function(violated_line, violation)

    fixed_line = "".join(fixed_line_list)
    lines[true_index] = fixed_line
    return lines
