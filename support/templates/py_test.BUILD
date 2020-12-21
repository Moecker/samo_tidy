load("@rules_python//python:defs.bzl", "py_test")

filegroup(
    name = "@TIDY_NAME_test_sources",
    srcs = glob([
        "data/*.cpp",
        "data/*.h",
    ]),
    visibility = ["//samo_tidy:__subpackages__"],
)

py_test(
    name = "test_@TIDY_NAME",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/checker/@TIDY_NAME/test:@TIDY_NAME_test_sources"],
    deps = [
        "//samo_tidy/checker/@TIDY_NAME",
        "//samo_tidy/checker/test:test_checker_lib",
    ],
)
