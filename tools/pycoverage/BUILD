load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")

package(default_visibility = ["//visibility:public"])

filegroup(
    name = "pycoverage_runner",
    srcs = [
        "pycoverage_runner.py",
    ],
)

py_library(
    name = "pycoverage",
    srcs = [
        "pycoverage_runner.py",
    ],
    deps = [requirement("coverage")],
)
