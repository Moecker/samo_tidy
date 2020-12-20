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


def fix_violations(violations, fix_function):
    """Applies a fix function for every violaton in a list"""
    for violation in violations:
        fix_violation(violation, fix_function)
