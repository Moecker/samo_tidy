load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "test_utils",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy:__subpackages__"],
    deps = ["//samo_tidy/utils"],
)

filegroup(
    name = "test_sources",
    srcs = glob([
        "data/*.cpp",
        "data/header/*.h",
    ]),
    visibility = ["//samo_tidy:__subpackages__"],
)
