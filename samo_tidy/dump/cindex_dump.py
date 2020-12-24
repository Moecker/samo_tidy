from clang import cindex
from optparse import OptionParser, OptionGroup
from pprint import pformat
from termcolor import colored
import argparse
import logging
import os
import sys

import samo_tidy.core.compdb_parser as compdb_parser
import samo_tidy.core.tu_parser as tu_parser
import samo_tidy.dump.dump as dump
import samo_tidy.utils.clang_setup as clang_setup
import samo_tidy.utils.diagnostics as diagnostics
import samo_tidy.utils.utils as utils


def get_basic_node_info(node, children):
    cleaned_children = [v for v in children if v is not None]
    return {
        "": cleaned_children,
        "kind": node.kind,
        "location": dump.pretty_location(node.location),
        "spelling": node.spelling,
    }


def get_detail_node_info(node, references):
    return {
        "is_definition": node.is_definition(),
        "location": node.location,
        "tokens": ",".join([token.spelling for token in node.get_tokens()]),
        "type": node.type.spelling,
        "usr": node.get_usr(),
        "xreferenced": f"{str(len(list(node.referenced.walk_preorder()))) if node.referenced else 0} times",
        "xreferences": references,
    }


def get_info(node, max_depth, depth, use_details, use_references):
    """Recursive call to get_info to obtain node properties returned as a dict"""
    if max_depth is not None and depth >= max_depth:
        children = None
    else:
        children = [get_info(child, max_depth, depth + 1, use_details, use_references) for child in node.get_children()]

    if node.location.file and utils.shall_ignore_based_on_file_name(node.location.file.name):
        return None

    info_dict = get_basic_node_info(node, children)

    if use_details:
        references = []
        if use_references:
            references = get_references(node, 1, 0)
        info_dict.update(get_detail_node_info(node, references))
    return info_dict


def get_references(node, max_depth, depth):
    """Recursive call to get_references to obtain referenced nodes returned as a dict"""
    if max_depth is not None and depth >= max_depth:
        references = get_basic_node_info(node, [])
    else:
        references = (
            [get_references(reference, max_depth, depth + 1) for reference in node.referenced.walk_preorder()]
            if node.referenced is not None
            else None
        )
    return references


def main():
    """Binary main entry point"""
    args = parse_args()
    logging.basicConfig(level=logging.INFO)
    clang_setup.setup_clang()

    the_file = args.file
    the_arguments = args.arguments

    # Use compdb infos if available
    if args.compdb:
        the_file, the_arguments = parse_from_compdb(args.compdb, args.file)
        if the_file == None:
            sys.exit(f"ERROR: File '{args.file}'' not found in compdb")

    # Only parse the file provided by the args
    logging.info(colored("Parsing file %s", "cyan"), the_file)
    logging.info(colored("Using arguments\n%s", "cyan"), pformat(the_arguments))
    translation_unit = tu_parser.create_translation_unit(the_file, the_arguments)
    if not translation_unit:
        sys.exit(f"ERROR: Unable to load input for file '{the_file}'")

    # Dump the content
    if not args.diagnostics_only:
        tu_dump = get_info(translation_unit.cursor, args.max_depth, 0, args.details, args.references)
        logging.info(
            colored(
                pformat(("nodes", tu_dump), width=120),
                attrs=["dark"],
            )
        )

    # Dump the diagnostics
    tu_diags = [diagnostics.get_diag_info(diagnostic) for diagnostic in translation_unit.diagnostics]
    logging.info(colored(pformat(("diagnostics", tu_diags)), "yellow"))

    sys.exit(0)


def parse_args():
    """Parse args and returns args dict"""
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
    parser.add_argument("--references", help="Show references of each node", action="store_true", default=False)
    parser.add_argument(
        "--max_depth",
        help="Limit cursor expansion to depth",
        type=int,
        default=None,
    )

    args = parser.parse_args()
    return args


def parse_from_compdb(compdb, file_to_parse):
    """Extracts the absolute file path of the file to parse and its arguments from compdb"""
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
        sys.exit("ERROR: Failed to load compdb")
    return absolute_filepath, file_arguments


if __name__ == "__main__":
    main()
