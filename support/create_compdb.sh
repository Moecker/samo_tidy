#!/bin/bash

set -euo pipefail

# https://github.com/grailbio/bazel-compilation-database/blob/0.4.5/README.md
bazel build //examples/example_cc_library:example_compdb

OUTFILE="$(bazel info bazel-bin)/examples/example_cc_library/compile_commands.json"
EXECROOT=$(bazel info execution_root)

sed -i.bak "s@__EXEC_ROOT__@${EXECROOT}@" "${OUTFILE}"

echo "INFO: Compilation Database is located in: ${OUTFILE}"
echo "INFO: Compilation Database looks like:"
echo "$(tail ${OUTFILE})"
