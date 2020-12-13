load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_compdb_parser",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_sources"],
    visibility = ["//samo_tidy/test:__pkg__"],
    deps = [
        "//samo_tidy/core",
        "//samo_tidy/test:test_utils",
        "//samo_tidy/utils",
    ],
)
