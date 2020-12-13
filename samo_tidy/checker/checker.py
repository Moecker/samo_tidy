import logging

from pprint import pprint, pformat
from clang import cindex

import samo_tidy.checker.violation as violations


def debug_token_contains(token):
    for child_token in token.get_tokens():
        logging.debug("Token contains: '%s'", child_token.spelling)


def debug_token_spelling(token):
    logging.debug("Token spelling is '%s':", pformat(token.type.spelling))


def get_ignored_file_strings():
    return ["/usr/", "/lib/gcc/"]


def shall_ignore_based_on_file_name(file_name):
    return any(word in file_name for word in get_ignored_file_strings())


def extract_violation(child_token, rule_id, message):
    location = child_token.location
    if any(word in location.file.name for word in get_ignored_file_strings()):
        logging.info("Ignoring violation from external file '%s'", location.file.name)
        return None
    violation = violations.Violation(
        rule_id,
        message,
        location.file.name,
        location.line,
        location.column,
    )
    logging.error(violation)
    return violation


def apply_checker(translation_unit, checker):
    violations = []
    ignored_violations = 0
    logging.info("Analyzing translation unit '%s'", translation_unit.spelling)
    if shall_ignore_based_on_file_name(translation_unit.spelling):
        logging.warning("Ignoring translation unit '%s'", translation_unit.spelling)
        return []
    for token in translation_unit.cursor.walk_preorder():
        violation = checker(token)
        if violation:
            violations.append(violation)
        else:
            ignored_violations += 1

    if ignored_violations > 0:
        logging.warning("Ignored %d violation(s) from external files", ignored_violations)
    return violations
