load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_@TIDY_NAME",
    srcs = glob(["**/*.py"]),
    deps = ["//samo_tidy/checker/test:test_checker_lib"],
)
