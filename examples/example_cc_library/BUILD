load("@rules_cc//cc:defs.bzl", "cc_library")
load("@bazel_compdb//:aspects.bzl", "compilation_database")

cc_library(
    name = "example_cc_library",
    srcs = glob(["**/*.cpp"]),
)

compilation_database(
    name = "example_compdb",
    targets = [
        "//examples/example_cc_library",
    ],
)
