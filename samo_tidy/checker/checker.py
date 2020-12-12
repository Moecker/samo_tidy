import logging

import clang
from clang import cindex
from pprint import pprint, pformat


def check_for_ints(translation_unit):
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.INTEGER_LITERAL:
            logging.debug("Token spelling is %s:", pformat(token.type.spelling))
            for child_token in token.get_tokens():
                logging.debug("Token contains: %s", child_token.spelling)
            if token.type.spelling == "unsigned int":
                for child_token in token.get_tokens():
                    if "u" in child_token.spelling:
                        logging.warning(
                            "TIDY_SUFFIX_CASE:%s:%s:%s",
                            child_token.location.file.name,
                            child_token.location.line,
                            child_token.location.column,
                        )
