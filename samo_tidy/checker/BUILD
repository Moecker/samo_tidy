load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "checker",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/core:__pkg__",
        "//samo_tidy/facade:__pkg__",
        "//samo_tidy/test:__pkg__",
    ],
    deps = [requirement("clang")],
)
