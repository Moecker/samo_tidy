load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

filegroup(
    name = "pylint_runner",
    srcs = [
        "pylint_runner.py",
    ],
)

py_library(
    name = "pylint",
    srcs = [
        "pylint_runner.py",
    ],
    deps = [requirement("pylint")],
)
