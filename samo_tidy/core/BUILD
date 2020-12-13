load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "core",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/checker:__pkg__",
        "//samo_tidy/core/test:__pkg__",
        "//samo_tidy/facade:__pkg__",
    ],
    deps = [requirement("clang")],
)
