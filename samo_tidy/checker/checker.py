import logging

from pprint import pprint, pformat
from clang import cindex

import samo_tidy.checker.violation as violations
import samo_tidy.utils.utils as utils


def debug_token_contains(token):
    for child_token in token.get_tokens():
        logging.debug("Token contains: '%s'", child_token.spelling)


def debug_token_spelling(token):
    logging.debug("Token spelling is '%s':", pformat(token.type.spelling))


def get_ignored_file_strings():
    return ["/usr/", "/lib/gcc/"]


def shall_ignore_based_on_file_name(file_name):
    return any(word in file_name for word in get_ignored_file_strings())


def extract_violation(token, rule_id, message):
    location = token.location
    if not location.file:
        logging.warning("Missing source location for '%s'", token.kind)
        return None
    if shall_ignore_based_on_file_name(location.file.name):
        # TODO Too noisy, add a "verbose" log level
        # logging.debug("Ignoring violation from external file '%s'", location.file.name)
        return None
    violation = violations.Violation(
        rule_id,
        message,
        location.file.name,
        location.line,
        location.column,
    )
    # The actual log out which can be mechanically read
    logging.error(violation)
    return violation


def apply_checker(translation_unit, checker):
    violations = []
    logging.info(
        "Analyzing translation unit '%s' with checker '%s'",
        utils.only_filename(translation_unit.spelling),
        checker.__module__,
    )

    # Only check non-external translation units
    if shall_ignore_based_on_file_name(translation_unit.spelling):
        logging.debug("Ignoring translation unit '%s'", utils.only_filename(translation_unit.spelling))
        return []

    # Decide based on the name of the function on which level the check shall be applied
    if checker.__name__ == "token_based_rule":
        for token in translation_unit.cursor.walk_preorder():
            violation = checker(token)
            if violation:
                violations.append(violation)
    elif checker.__name__ == "translation_unit_based_rule":
        violations = checker(translation_unit)
    return violations
