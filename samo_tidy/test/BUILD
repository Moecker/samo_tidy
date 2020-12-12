load("@rules_python//python:defs.bzl", "py_test")

# TODO Move all test targets to their packages
py_test(
    name = "test_facade",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy/test:__pkg__"],
    deps = ["//samo_tidy/facade"],
)

py_test(
    name = "test_checker",
    srcs = glob(["**/*.py"]),
    data = glob(["data/*.cpp"]),
    visibility = ["//samo_tidy/test:__pkg__"],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_compdb_parser",
    srcs = glob(["**/*.py"]),
    data = ["data/source_id1.cpp"],
    visibility = ["//samo_tidy/test:__pkg__"],
    deps = [
        "//samo_tidy/core",
        "//samo_tidy/utils",
    ],
)
