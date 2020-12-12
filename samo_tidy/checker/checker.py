import logging

import clang
from clang import cindex
from pprint import pprint, pformat


from samo_tidy.checker.violation import Violation


def debug_token_contains(token):
    for child_token in token.get_tokens():
        logging.debug("Token contains: %s", child_token.spelling)


def debug_token_spelling(token):
    logging.debug("Token spelling is %s:", pformat(token.type.spelling))


def get_ignored_file_strings():
    return ["/usr/", "/lib/gcc/"]


def check_for_ints(translation_unit):
    violations = []
    no_ignored_violations = 0
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.INTEGER_LITERAL:
            if token.type.spelling == "unsigned int":
                for child_token in token.get_tokens():
                    if "u" in child_token.spelling:
                        location = child_token.location
                        if any(word in location.file.name for word in get_ignored_file_strings()):
                            logging.debug("Ignoring violation from external file %s", location.file.name)
                            no_ignored_violations += 1
                            continue
                        violation = Violation(
                            "TIDY_SUFFIX_CASE",
                            location.file.name,
                            location.line,
                            location.column,
                        )
                        violations.append(violation)
                        logging.error(violation)
    if no_ignored_violations > 0:
        logging.warning("Ignored %d violation(s) from external files", no_ignored_violations)
    return violations
