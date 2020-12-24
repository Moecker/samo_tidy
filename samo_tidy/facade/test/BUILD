load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "test_facade_lib",
    srcs = glob(["**/*.py"]),
    data = [
        "//samo_tidy/test:test_compdb",
        "//samo_tidy/test:test_multiple_files_compdb",
    ],
    deps = [
        "//samo_tidy/facade",
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_parallel_facade",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/facade/test:test_facade_lib",
    ],
)

py_test(
    name = "test_serial_facade",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/facade/test:test_facade_lib",
    ],
)
