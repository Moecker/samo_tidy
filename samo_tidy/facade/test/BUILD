load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_facade",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_compdb"],
    deps = [
        "//samo_tidy/facade",
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_parallel_facade",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_multiple_files_compdb"],
    deps = [
        "//samo_tidy/facade",
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)
