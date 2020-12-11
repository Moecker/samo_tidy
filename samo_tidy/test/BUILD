load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_run",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy/test:__pkg__"],
    deps = ["//samo_tidy/core"],
)

py_test(
    name = "test_compdb_parser",
    srcs = glob(["**/*.py"]),
    data = ["data/source_id1.cpp"],
    visibility = ["//samo_tidy/test:__pkg__"],
    deps = ["//samo_tidy/core"],
)
