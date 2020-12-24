load("@rules_python//python:defs.bzl", "py_test")

pycoverage_requirements = [
    "//tools/pycoverage",
]

def pycoverage(name, deps):
    if not name or not deps:
        fail("Arguments 'name' and 'deps' are required")

    py_test(
        name = name,
        main = "pycoverage_runner.py",
        srcs = ["//tools/pycoverage:pycoverage_runner"],
        imports = ["."],
        args = deps,
        deps = depset(direct = deps + pycoverage_requirements).to_list(),
    )
