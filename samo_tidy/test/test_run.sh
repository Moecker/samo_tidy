#!/bin/bash

set -euo pipefail

readlinkf() { perl -MCwd -e 'print Cwd::abs_path shift' "${1}"; }

ABSPATH="$(readlinkf ${0})"
BAZEL_ROOT="$(dirname ${ABSPATH})"

pushd "${BAZEL_ROOT}"
    bazel run //samo_tidy/facade:run -- --help
    bazel run //samo_tidy/facade:run_parallel -- --help
popd
