load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "utils",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy:__subpackages__"],
    deps = [requirement("clang")],
)

py_binary(
    name = "cindex_dump",
    srcs = ["cindex_dump.py"],
    visibility = ["//samo_tidy:__subpackages__"],
    deps = [
        requirement("clang"),
        "//samo_tidy/utils",
    ],
)
