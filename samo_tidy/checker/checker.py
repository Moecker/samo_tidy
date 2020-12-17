from clang import cindex
from pprint import pprint, pformat
from termcolor import colored
import logging

import samo_tidy.checker.violation as violations
import samo_tidy.core.summary as summary
import samo_tidy.utils.utils as utils


def debug_token_contains(token):
    for child_token in token.get_tokens():
        logging.debug("Token contains: '%s'", child_token.spelling)


def debug_token_spelling(token):
    logging.debug("Token spelling is '%s':", pformat(token.type.spelling))


def present_violation(violation):
    # The actual log out which can be mechanically read
    logging.warning(colored(violation, "blue"))
    logging.error(colored(violation.style(), "yellow"))
    # TODO logging.info(colored(violation.file_path_link(), "green"))


def extract_violation(token, rule_id, message):
    location = token.location
    if not location.file:
        logging.warning("Missing source location for '%s', skipping", token.kind)
        return None
    if utils.shall_ignore_based_on_file_name(location.file.name):
        logging.debug("Ignoring violation for id '%s' from file '%s'", rule_id, location.file.name)
        summary.get_summary().add_ignored_translation_unit(utils.only_filename(location.file.name))
        return None
    violation = violations.Violation(
        rule_id,
        message,
        location.file.name,
        location.line,
        location.column,
    )
    summary.get_summary().add_filename(location.file.name)
    present_violation(violation)
    return violation


def apply_checker(translation_unit, checker):
    # TODO Most checkers traverse the tu again and again, this can be speed up
    violations = []
    logging.info(
        colored("Analyzing translation unit '%s' with checker '%s'", "cyan"),
        utils.only_filename(translation_unit.spelling),
        checker.__module__,
    )

    # Only check non-external translation units
    if utils.shall_ignore_based_on_file_name(translation_unit.spelling):
        logging.debug("Ignoring translation unit '%s'", utils.only_filename(translation_unit.spelling))
        summary.get_summary().add_ignored_translation_unit(utils.only_filename(translation_unit.spelling))
        return []

    # Decide based on the name of the function on which level the check shall be applied
    if checker.__name__ == "token_based_rule":
        for token in translation_unit.cursor.walk_preorder():
            violation = checker(token)
            if violation:
                violations.append(violation)

    elif checker.__name__ == "translation_unit_based_rule":
        violations = checker(translation_unit)

    # TODO Consider returning diagnostics
    return violations
