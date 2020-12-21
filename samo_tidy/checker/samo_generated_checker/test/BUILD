load("@rules_python//python:defs.bzl", "py_test")

filegroup(
    name = "samo_generated_checker_test_sources",
    srcs = glob([
        "data/*.cpp",
        "data/*.h",
    ]),
    visibility = ["//samo_tidy:__subpackages__"],
)

py_test(
    name = "test_samo_generated_checker",
    srcs = glob(["**/*.py"]),
    data = ["//samo_tidy/checker/samo_generated_checker/test:samo_generated_checker_test_sources"],
    deps = [
        "//samo_tidy/checker/samo_generated_checker",
        "//samo_tidy/checker/test:test_checker_lib",
    ],
)
