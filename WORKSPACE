workspace(name = "samo_tidy")

# https://github.com/bazelbuild/rules_python/blob/0.1.0/README.md
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# https://github.com/bazelbuild/rules_python/blob/0.1.0/README.md
http_archive(
    name = "rules_python",
    sha256 = "b6d46438523a3ec0f3cead544190ee13223a52f6a6765a29eae7b7cc24cc83a0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.1.0/rules_python-0.1.0.tar.gz",
)

# https://github.com/bazelbuild/rules_python/blob/0.1.0/README.md
load("@rules_python//python:pip.bzl", "pip_install")

# https://github.com/bazelbuild/rules_python/blob/0.1.0/README.md
pip_install(
    requirements = "//:requirements.txt",
)

# https://github.com/grailbio/bazel-compilation-database/blob/0.4.5/README.md
http_archive(
    name = "bazel_compdb",
    sha256 = "bcecfd622c4ef272fd4ba42726a52e140b961c4eac23025f18b346c968a8cfb4",
    strip_prefix = "bazel-compilation-database-0.4.5",
    urls = ["https://github.com/grailbio/bazel-compilation-database/archive/0.4.5.tar.gz"],
)
