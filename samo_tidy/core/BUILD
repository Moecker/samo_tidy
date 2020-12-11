load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "core",
    srcs = glob([
        "**/*.py",
    ]),
    visibility = [
        "//samo_tidy/test:__pkg__",
    ],
    deps = [
        requirement("clang"),
    ],
)

py_binary(
    name = "run",
    srcs = ["run.py"],
    deps = [":core"],
)
