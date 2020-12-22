load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "facade",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy/facade/test:__pkg__"],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/checker:checkers",
        "//samo_tidy/core",
        "//samo_tidy/fixit",
        "//samo_tidy/utils",
    ],
)

py_binary(
    name = "run",
    srcs = glob(["**/*.py"]),
    main = "serial_facade.py",
    deps = [
        "//samo_tidy/facade",
    ],
)

py_binary(
    name = "run_parallel",
    srcs = glob(["**/*.py"]),
    main = "parallel_facade.py",
    deps = [
        "//samo_tidy/facade",
    ],
)
