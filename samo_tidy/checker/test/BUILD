load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_clang_warning_checker",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy/test:__pkg__"],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/test:test_utils",
    ],
)
