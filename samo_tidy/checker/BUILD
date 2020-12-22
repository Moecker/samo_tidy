load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "checker",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/checker/test:__pkg__",
        "//samo_tidy/facade:__pkg__",
        "//samo_tidy/fixit:__pkg__",
    ],
    deps = [
        requirement("clang"),
        requirement("termcolor"),
        "//samo_tidy/core",
    ],
)

py_library(
    name = "checkers",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/checker/test:__pkg__",
        "//samo_tidy/facade:__pkg__",
        "//samo_tidy/fixit:__pkg__",
    ],
    deps = [
        "//samo_tidy/checker/samo_class_name_checker",
        "//samo_tidy/checker/samo_missing_const_checker",
        "//samo_tidy/checker/samo_multiple_classes_checker",
        "//samo_tidy/checker/samo_nested_namespaces_checker",
        "//samo_tidy/checker/samo_suffix_case_checker",
    ],
)
