import logging

import clang
from clang import cindex
from pprint import pprint, pformat


from samo_tidy.checker.violation import Violation


def check_for_ints(translation_unit):
    violations = []
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.INTEGER_LITERAL:
            logging.debug("Token spelling is %s:", pformat(token.type.spelling))
            for child_token in token.get_tokens():
                logging.debug("Token contains: %s", child_token.spelling)
            if token.type.spelling == "unsigned int":
                for child_token in token.get_tokens():
                    if "u" in child_token.spelling:
                        location = child_token.location
                        violation = Violation(
                            "TIDY_SUFFIX_CASE",
                            location.file.name,
                            location.line,
                            location.column,
                        )
                        violations.append(violation)
                        logging.warning(violation)
    return violations
