from clang import cindex
from optparse import OptionParser, OptionGroup
from pprint import pprint, pformat
import argparse
import logging

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.utils as utils
import samo_tidy.dump.dump as dump


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
            "location (ignored)": node.location,
        }
    else:
        return {
            "kind": node.kind,
            "usr": node.get_usr(),
            "spelling": node.spelling,
            "location": node.location,
            "is_definition": node.is_definition(),
            "->": children,
            "tokens": ",".join([token.spelling for token in node.get_tokens()]),
        }


def parse_from_compdb(args):
    compdb = compdb_parser.load_compdb(args.compdb)
    commands = compdb.getAllCompileCommands()
    for command in commands:
        if args.file in command.filename:
            the_file = command.filename
            the_arguments = list(command.arguments)
            the_arguments = tu_parser.clean_args(the_arguments)
            the_arguments = tu_parser.absolute_path_include(the_arguments, command.directory)
    return the_file, the_arguments


def parse_args():
    parser = argparse.ArgumentParser("CIndex Dump")
    parser.add_argument("--file", help="Filepath to be analyzed", required=True)
    parser.add_argument("--compdb", help="Compilation Database for detailed build instructions")
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

    the_file = args.file
    the_arguments = args.arguments

    index = cindex.Index.create()

    # Use compdb infos if available
    if args.compdb:
        the_file, the_arguments = parse_from_compdb(args)

    # Only parse the file provided by the args
    tu = index.parse(the_file, the_arguments)
    if not tu:
        logging.error("Unable to load input")

    # Dump the tu content
    pprint(("diags", [dump.get_diag_info(d) for d in tu.diagnostics]))

    # Dump the diagnostics
    if not args.diagnostics_only:
        pprint(("nodes", get_info(tu.cursor, args.max_depth)))


if __name__ == "__main__":
    main()
