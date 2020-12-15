load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_utils",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)
