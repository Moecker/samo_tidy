def check_for_clang_warnings(translation_unit):
    violations = []
    no_ignored_violations = 0
    for diagnostic in translation_unit.diagnostics:
        print(diagnostic)
        violations.append(diagnostic)
    return violations
