load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "core",
    srcs = glob(["**/*.py"]),
    visibility = [
        "//samo_tidy/checker:__subpackages__",
        "//samo_tidy/core/test:__pkg__",
        "//samo_tidy/dump:__pkg__",
        "//samo_tidy/facade:__pkg__",
        "//samo_tidy/utils/test:__pkg__",
    ],
    deps = [
        requirement("clang"),
        requirement("termcolor"),
    ],
)
