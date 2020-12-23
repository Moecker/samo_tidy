import samo_tidy.utils.utils as utils


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
