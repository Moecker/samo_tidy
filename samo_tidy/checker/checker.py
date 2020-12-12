import logging

import clang
from clang import cindex
from pprint import pprint, pformat


def check_for_ints(translation_unit):
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.INTEGER_LITERAL:
            logging.debug(pformat(dir(token)))
            logging.debug("Token spelling is %s:", pformat(token.type.spelling))
            logging.debug(pformat(dir(token.type)))