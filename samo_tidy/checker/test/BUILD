load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "test_checker_lib",
    srcs = glob(["**/*.py"]),
    data = [
        "//samo_tidy/test:test_sources",
    ],
    visibility = ["//samo_tidy/checker:__subpackages__"],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/checker:checkers",
        "//samo_tidy/dump",
        "//samo_tidy/fixit",
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_checker",
    srcs = glob(["**/*.py"]),
    deps = ["//samo_tidy/checker/test:test_checker_lib"],
)

py_test(
    name = "test_clang_warning_checker",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/test:test_support",
    ],
)
