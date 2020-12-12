load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "core",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/facade:__pkg__",
        "//samo_tidy/test:__pkg__",
    ],
    deps = [requirement("clang")],
)

