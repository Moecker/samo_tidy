load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")
load("//tools/pylint:pylint.bzl", "pylint")

py_library(
    name = "utils",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy:__subpackages__"],
    deps = [
        requirement("clang"),
        requirement("termcolor"),
    ],
)

pylint(
    name = "pylint",
    modules = ["samo_tidy.utils"],
    deps = [
        ":utils",
    ],
)
