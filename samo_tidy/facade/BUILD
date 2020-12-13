load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "facade",
    srcs = ["facade.py"],
    visibility = [
        "//samo_tidy/test:__pkg__",
    ],
    deps = [
        "//samo_tidy/checker",
        "//samo_tidy/core",
        "//samo_tidy/utils",
    ],
)

py_binary(
    name = "run",
    srcs = ["facade.py"],
    main = "facade.py",
    deps = [
        "//samo_tidy/facade",
    ],
)
