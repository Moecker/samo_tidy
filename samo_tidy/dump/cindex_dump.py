from clang import cindex
from optparse import OptionParser, OptionGroup
from pprint import pprint, pformat
import argparse
import logging
import os
import sys
from termcolor import colored

import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.utils as utils
import samo_tidy.dump.dump as dump


def get_info(node, max_depth, depth, details):
    if max_depth is not None and depth >= max_depth:
        children = None
    else:
        children = [get_info(c, max_depth, depth + 1, details) for c in node.get_children()]

    if node.location.file and utils.shall_ignore_based_on_file_name(node.location.file.name):
        return

    info_dict = {
        "kind": node.kind,
        "spelling": node.spelling,
        "location": dump.pretty_location(node.location),
        "<--": children,
    }
    if details:
        info_dict.update(
            {
                "tokens": ",".join([token.spelling for token in node.get_tokens()]),
                "usr": node.get_usr(),
                "location": node.location,
                "is_definition": node.is_definition(),
                "type": node.type.spelling,
                "referenced": node.referenced,
            }
        )
    return info_dict


def parse_from_compdb(compdb, file_to_parse):
    absolute_filepath = None
    file_arguments = []

    compdb = compdb_parser.load_compdb(compdb)
    if compdb:
        commands = compdb.getAllCompileCommands()
        for command in commands:
            if file_to_parse in command.filename:
                absolute_filepath = os.path.join(command.directory, command.filename)
                file_arguments = list(command.arguments)
                file_arguments = tu_parser.clean_args(file_arguments)
                file_arguments = tu_parser.absolute_path_include(file_arguments, command.directory)
    else:
        sys.exit("Failed to load compdb")
    return absolute_filepath, file_arguments


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
    parser.add_argument("--details", help="Show more details per node", action="store_true", default=False)
    parser.add_argument(
        "--max_depth",
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
        the_file, the_arguments = parse_from_compdb(args.compdb, args.file)
        if the_file == None:
            sys.exit(f"File '{args.file}'' not found in compdb")

    # Only parse the file provided by the args
    logging.info("Parsing %s with %s", the_file, the_arguments)
    translation_unit = tu_parser.create_translation_unit(the_file, the_arguments)
    if not translation_unit:
        sys.exit(f"Unable to load input for file '{the_file}'")

    # Dump the tu content
    if not args.diagnostics_only:
        start_depth = 0
        logging.info(
            colored(
                pformat(("nodes", get_info(translation_unit.cursor, args.max_depth, start_depth, args.details))),
                attrs=["dark"],
            )
        )

    # Dump the diagnostics
    logging.info(
        pformat(("diagnostics", [dump.get_diag_info(diagnostic) for diagnostic in translation_unit.diagnostics]))
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
