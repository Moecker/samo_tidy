load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "fixit",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/facade:__pkg__",
        "//samo_tidy/fixit/test:__pkg__",
    ],
    deps = ["//samo_tidy/checker"],
)
