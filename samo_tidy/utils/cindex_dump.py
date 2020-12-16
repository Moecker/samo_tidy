from clang.cindex import Index
from optparse import OptionParser, OptionGroup
from pprint import pprint, pformat
import argparse
import logging

import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.utils as utils


def get_diag_info(diag):
    return {
        "severity": diag.severity,
        "location": diag.location,
        "spelling": diag.spelling,
        "ranges": diag.ranges,
        "fixits": diag.fixits,
    }


def dump_node(node):
    return "\n" + pformat(
        {
            "kind": node.kind,
            "spelling": node.spelling,
            "location": node.location,
            "is_definition": node.is_definition(),
        }
    )


def get_cursor_id(cursor, cursor_list=[]):
    if cursor is None:
        return None

    # TODO: This is really slow. It would be nice if the index API exposed something that let us hash cursors.
    for i, c in enumerate(cursor_list):
        if cursor == c:
            return i
    cursor_list.append(cursor)
    return len(cursor_list) - 1


def get_info(node, max_depth=None, depth=0):
    if max_depth is not None and depth >= max_depth:
        children = None
    else:
        if node.location.file and "/usr" in node.location.file.name:
            children = None
        else:
            children = [get_info(c, max_depth, depth + 1) for c in node.get_children()]
    if node.location.file and "/usr" in node.location.file.name:
        return {
            "location": node.location,
        }
    else:
        return {
            "id": get_cursor_id(node),
            "kind": node.kind,
            "usr": node.get_usr(),
            "spelling": node.spelling,
            "location": node.location,
            "extent.start": node.extent.start,
            "extent.end": node.extent.end,
            "is_definition": node.is_definition(),
            "definition id": get_cursor_id(node.get_definition()),
            "->": children,
            "number_of_tokens": len(list(node.get_tokens())),
            "tokens": ",".join([token.spelling for token in node.get_tokens()]),
        }


def parse_args():
    parser = argparse.ArgumentParser("CIndex Dump")
    parser.add_argument("--file", help="Filepath to be analyzed", required=True)
    parser.add_argument(
        "--arguments",
        help="Arguments for parsing the file (such as -I flags)",
        default=[],
        nargs="+",
    )
    parser.add_argument("--diagnostics_only", help="Only show diagnostics", action="store_true", default=False)
    parser.add_argument(
        "--max-depth",
        help="Limit cursor expansion to depth",
        type=int,
        default=None,
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    logging.basicConfig(level=logging.DEBUG)
    clang_setup.setup_clang()

    index = Index.create()
    tu = index.parse(args.file, args.arguments)
    if not tu:
        logging.error("Unable to load input")

    pprint(("diags", [get_diag_info(d) for d in tu.diagnostics]))
    if not args.diagnostics_only:
        pprint(("nodes", get_info(tu.cursor, args.max_depth)))


if __name__ == "__main__":
    main()
