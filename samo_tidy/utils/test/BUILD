load("@rules_python//python:defs.bzl", "py_test")
load("//tools/pycoverage:pycoverage.bzl", "pycoverage")

py_test(
    name = "test_utils",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)

pycoverage(
    name = "pycoverage",
    deps = [":test_utils"],
)
