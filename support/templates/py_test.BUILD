load("@rules_python//python:defs.bzl", "py_test")

filegroup(
    name = "__TIDY_NAME___test_sources",
    srcs = glob([
        "data/*.cpp",
        "data/*.h",
    ]),
    visibility = ["//samo_tidy:__subpackages__"],
)

py_test(
    name = "test___TIDY_NAME__",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/checker/__TIDY_NAME__/test:__TIDY_NAME___test_sources"],
    deps = [
        "//samo_tidy/checker/__TIDY_NAME__",
        "//samo_tidy/checker/test:test_checker_lib",
    ],
)
