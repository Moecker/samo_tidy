load("@rules_python//python:defs.bzl", "py_test")

pylint_requirements = [
    "//tools/pylint",
]

def pylint(name, modules, deps = []):
    if not name or not modules:
        fail("Arguments 'name' and 'modules' are required")

    py_test(
        name = name,
        main = "pylint_runner.py",
        srcs = ["//tools/pylint:pylint_runner"],
        imports = ["."],
        args = ["--modules " + " ".join(modules)],
        deps = depset(direct = deps + pylint_requirements).to_list(),
    )
