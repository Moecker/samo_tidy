load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "dump",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy:__subpackages__"],
    deps = [
        requirement("clang"),
        "//samo_tidy/core",
        "//samo_tidy/utils",
    ],
)

py_binary(
    name = "cindex_dump",
    srcs = ["cindex_dump.py"],
    visibility = ["//samo_tidy:__subpackages__"],
    deps = [
        "//samo_tidy/dump",
    ],
)
