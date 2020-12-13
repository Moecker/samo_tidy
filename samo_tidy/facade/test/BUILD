load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_facade",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy/facade/test:__pkg__"],
    deps = [
        "//samo_tidy/facade",
        "//samo_tidy/test:test_utils",
    ],
)
