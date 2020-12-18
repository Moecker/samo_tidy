load("@rules_python//python:defs.bzl", "py_test")

py_test(
    name = "test_dump",
    srcs = glob(["**/*.py"]),
    deps = [
        "//samo_tidy/dump",
        "//samo_tidy/test:test_support",
    ],
)

py_test(
    name = "test_cindex_dump",
    srcs = glob(["**/*.py"]),
    data = [
        "//samo_tidy/test:test_sources",
        "//samo_tidy/test:test_sources_compdb",
    ],
    deps = [
        "//samo_tidy/dump",
        "//samo_tidy/test:test_support",
    ],
)
