import logging

from pprint import pprint
from optparse import OptionParser, OptionGroup
from clang.cindex import Index

from samo_tidy.utils.utils import setup_clang


def get_diag_info(diag):
    return {
        "severity": diag.severity,
        "location": diag.location,
        "spelling": diag.spelling,
        "ranges": diag.ranges,
        "fixits": diag.fixits,
    }


def get_cursor_id(cursor, cursor_list=[]):
    if cursor is None:
        return None

    # TODO: This is really slow. It would be nice if the index API exposed
    # something that let us hash cursors.
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


def main():
    parser = OptionParser("usage: %prog [options] {filename} [clang-args*]")

    parser.add_option(
        "--diagnosis_only", dest="diagnosis_only", help="Only show diagnosis", action="store_true", default=False
    )
    parser.add_option(
        "--max-depth",
        dest="max_depth",
        help="Limit cursor expansion to depth N",
        metavar="N",
        type=int,
        default=None,
    )
    parser.disable_interspersed_args()
    (opts, args) = parser.parse_args()

    if len(args) == 0:
        parser.error("invalid number arguments")

    logging.basicConfig(level=logging.DEBUG)
    setup_clang()

    index = Index.create()
    tu = index.parse(None, args)
    if not tu:
        parser.error("unable to load input")

    pprint(("diags", [get_diag_info(d) for d in tu.diagnostics]))
    if not opts.diagnosis_only:
        pprint(("nodes", get_info(tu.cursor, opts.max_depth)))


if __name__ == "__main__":
    main()