import logging

from pprint import pprint, pformat
from clang import cindex

from samo_tidy.checker.violation import Violation


def debug_token_contains(token):
    for child_token in token.get_tokens():
        logging.debug("Token contains: '%s'", child_token.spelling)


def debug_token_spelling(token):
    logging.debug("Token spelling is '%s':", pformat(token.type.spelling))


def get_ignored_file_strings():
    return ["/usr/", "/lib/gcc/"]


def extract_violation(child_token, rule_id):
    location = child_token.location
    if any(word in location.file.name for word in get_ignored_file_strings()):
        logging.debug("Ignoring violation from external file '%s'", location.file.name)
        no_ignored_violations += 1
        return None
    violation = Violation(
        rule_id,
        location.file.name,
        location.line,
        location.column,
    )
    logging.error(violation)
    return violation


def check_for_ints(translation_unit):
    violations = []
    no_ignored_violations = 0
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.INTEGER_LITERAL:
            if token.type.spelling == "unsigned int":
                for child_token in token.get_tokens():
                    violation = None
                    if "u" in child_token.spelling:
                        violation = extract_violation(child_token, "TIDY_SUFFIX_CASE")
                    if not "u" in child_token.spelling.lower():
                        violation = extract_violation(child_token, "TIDY_SUFFIX_MISSING")
                    if violation:
                        violations.append(violation)
    if no_ignored_violations > 0:
        logging.warning("Ignored %d violation(s) from external files", no_ignored_violations)
    return violations
