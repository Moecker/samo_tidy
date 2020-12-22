load("@rules_python//python:defs.bzl", "py_library")

py_library(
    name = "test_support",
    srcs = glob(["**/*.py"]),
    visibility = ["//samo_tidy:__subpackages__"],
    deps = ["//samo_tidy/utils"],
)

filegroup(
    name = "test_sources",
    srcs = glob([
        "data/cpp_files/*.cpp",
        "data/cpp_files/header/*.h",
    ]),
    visibility = ["//samo_tidy:__subpackages__"],
)

filegroup(
    name = "test_sources_compdb",
    srcs = ["data/cpp_files_compdb/compile_commands.json"],
    visibility = ["//samo_tidy:__subpackages__"],
)

filegroup(
    name = "test_compdb",
    srcs = ["data/single_file_compdb/compile_commands.json"],
    visibility = ["//samo_tidy:__subpackages__"],
)

filegroup(
    name = "test_multiple_files_compdb",
    srcs = ["data/multiple_files_compdb/compile_commands.json"],
    visibility = ["//samo_tidy:__subpackages__"],
)

# This is a lazy test which calls the facade on a working local setup.
# Deactivate or adapt to your needs.
sh_test(
    name = "test_run",
    srcs = ["test_run.sh"],
    tags = ["manual"],
)
