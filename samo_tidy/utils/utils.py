import logging
from pprint import pformat
import clang
from clang import cindex


def setup_clang():
    cindex.Config.set_library_file("/usr/local/opt/llvm/lib/libclang.dylib")


def debug_file_content(file_path):
    with open(file_path) as f:
        logging.debug("File %s looks like: %s", file_path, pformat(f.readlines()))


def traverse(node, level):
    print(
        "%s %-35s %-20s %-10s [%-6s:%s - %-6s:%s] %s %s "
        % (
            " " * level,
            node.kind,
            node.spelling,
            node.type.spelling,
            node.extent.start.line,
            node.extent.start.column,
            node.extent.end.line,
            node.extent.end.column,
            node.location.file,
            node.mangled_name,
        )
    )
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        for arg in node.get_arguments():
            print("ARG=%s %s" % (arg.kind, arg.spelling))

    for child in node.get_children():
        traverse(child, level + 1)
