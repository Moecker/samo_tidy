import samo_tidy.utils.utils as utils


def get_diag_info(diag):
    return {
        "severity": diag.severity,
        "location": diag.location,
        "spelling": diag.spelling,
        "ranges": diag.ranges,
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


def pretty_location(location):
    if location:
        if location.file:
            return f"{utils.only_filename(location.file.name)}:{location.line}:{location.column}"
    return location
