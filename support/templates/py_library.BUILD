load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "@TIDY_NAME",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/checker/@TIDY_NAME/test:__pkg__",
        "//samo_tidy/facade:__pkg__",
        "//samo_tidy/fixit:__pkg__",
    ],
    deps = [
        requirement("clang"),
        requirement("termcolor"),
        "//samo_tidy/core",
    ],
)
