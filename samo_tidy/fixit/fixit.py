from termcolor import colored
import importlib
import logging


def apply_fix_per_line(lines, violation, fix_function):
    """Apply fix function for lines"""
    checker_module = importlib.import_module(fix_function.__module__)
    if violation.id != checker_module.ID:
        return []
    true_index = violation.line - 1
    violated_line = list(lines[true_index])
    logging.info(colored(f"Fixing {violation}", "green"))

    fixed_line_list = fix_function(violated_line, violation)

    fixed_line = "".join(fixed_line_list)
    lines[true_index] = fixed_line
    return lines


def fix_violation_per_line(violation, fix_function):
    """Apply fix function for given violation, expects a line-violation"""
    lines = []
    with open(violation.file_path) as the_file:
        lines = the_file.readlines()

    fixed_lines = apply_fix_per_line(lines, violation, fix_function)

    if fixed_lines:
        with open(violation.file_path, "w") as the_file:
            the_file.writelines(fixed_lines)
    return fixed_lines


def fix_violations_per_line(violations, fix_function):
    """Applies a fix function for every violaton in a list"""
    for violation in violations:
        fix_violation_per_line(violation, fix_function)
