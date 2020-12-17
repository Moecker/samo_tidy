from clang import cindex

import samo_tidy.checker.checker as checker


def translation_unit_based_rule(translation_unit):
    violations = []
    for token in translation_unit.cursor.walk_preorder():
        if token.kind == cindex.CursorKind.VAR_DECL:
            if token.referenced:
                for reference in token.referenced.walk_preorder():
                    print(reference.location)
    return violations
