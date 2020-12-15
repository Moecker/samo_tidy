load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "test_checker_lib",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_sources"],
    visibility = [":__subpackages__"],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/test:test_utils",
        "//samo_tidy/utils",
    ],
)

py_test(
    name = "test_checker",
    srcs = glob(["**/*.py"]),
    deps = ["//samo_tidy/checker/test:test_checker_lib"],
)

py_test(
    name = "test_samo_suffix_case_checker",
    srcs = glob(["**/*.py"]),
    deps = ["//samo_tidy/checker/test:test_checker_lib"],
)

py_test(
    name = "test_samo_multiple_classes_checker",
    srcs = glob(["**/*.py"]),
    deps = ["//samo_tidy/checker/test:test_checker_lib"],
)

py_test(
    name = "test_samo_unsigned_int_checker",
    srcs = glob(["**/*.py"]),
    deps = ["//samo_tidy/checker/test:test_checker_lib"],
)

py_test(
    name = "test_clang_warning_checker",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/test:test_utils",
    ],
)
