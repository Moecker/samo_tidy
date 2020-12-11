load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_run",
    srcs = glob([
        "**/*.py",
    ]),
    visibility = [
        "//samo_tidy/test:__pkg__",
    ],
    deps = ["//samo_tidy/core"],
)
