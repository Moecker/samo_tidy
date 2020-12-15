load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "test_core_lib",
    srcs = glob(["**/*.py"]),
    visibility = [":__subpackages__"],
    deps = [
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_compdb_parser",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_sources"],
    deps = [
        "//samo_tidy/core",
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_parallel_parser",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_sources"],
    deps = [
        "//samo_tidy/core",
        "//samo_tidy/core/test:test_core_lib",
    ],
)
