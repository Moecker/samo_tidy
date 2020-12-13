load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_facade",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/test:test_compdb"],
    visibility = ["//samo_tidy/facade/test:__pkg__"],
    deps = [
        "//samo_tidy/facade",
        "//samo_tidy/test:test_utils",
        "//samo_tidy/utils",
    ],
)
