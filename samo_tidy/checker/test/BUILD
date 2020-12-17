load("@rules_python//python:defs.bzl", "py_library", "py_test")

py_library(
    name = "test_checker_lib",
    srcs = glob(["**/*.py"]),
    data = [
        "//samo_tidy/checker/test:test_sources",
        "//samo_tidy/test:test_sources",
    ],
    visibility = [":__subpackages__"],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/dump",
        "//samo_tidy/test:test_support",
        "//samo_tidy/utils",
    ],
)

filegroup(
    name = "test_sources",
    srcs = glob([
        "data/*.cpp",
        "data/*.h",
    ]),
    visibility = ["//samo_tidy/checker/test/__subpackages__"],
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
    name = "test_samo_nested_namespaces_checker",
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
        "//samo_tidy/test:test_support",
    ],
)

# TODO Add multiple namespace check
# TODO Add using count check
