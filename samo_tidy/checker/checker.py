import logging

import clang
from clang import cindex
from pprint import pprint
from inspect import getmembers


class Printer:
    def __init__(self, PrintableClass):
        for name in dir(PrintableClass):
            value = getattr(PrintableClass, name)
            if "_" not in str(name).join(str(value)):
                print("  .%s: %r" % (name, value))


def var_dump(var, prefix=""):
    """
    You know you're a php developer when the first thing you ask for
    when learning a new language is 'Where's var_dump?????'
    """
    my_type = "[" + var.__class__.__name__ + "(" + str(len(var)) + ")]:"
    print(prefix, my_type, sep="")
    prefix += "    "
    for i in var:
        if type(i) in (list, tuple, dict, set):
            var_dump(i, prefix)
        else:
            if isinstance(var, dict):
                print(prefix, i, ": (", var[i].__class__.__name__, ") ", var[i], sep="")
            else:
                print(prefix, "(", i.__class__.__name__, ") ", i, sep="")


def check_for_ints(translation_unit):
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.INTEGER_LITERAL:
            # Debug
            # print(dir(token))
            # print(dir(token.type))
            # print(token.type.spelling)

            var_dump([token])
            Printer(token)
