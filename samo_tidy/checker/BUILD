load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "checker",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/core:__pkg__",
        "//samo_tidy/test:__pkg__",
    ],
)
