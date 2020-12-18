load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_fixit",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/fixit",
        "//samo_tidy/test:test_support",
    ],
)
