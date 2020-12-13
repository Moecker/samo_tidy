load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_checker",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_sources"],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/test:test_utils",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_clang_warning_checker",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/test:test_utils",
    ],
)
