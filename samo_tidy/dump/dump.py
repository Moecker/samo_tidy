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
