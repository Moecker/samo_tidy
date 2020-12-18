#!/bin/bash

set -euo pipefail

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

usage() { echo \
"Usage: $0
  - Mandatory
      [-n Name of checker]
  - Optional
      [-l Location
  - Flags
      [-r Register checker in config]
  - Help
      [-h Show this help]" \
1>&2; }

if [ $# -eq 0 ]; then
  usage
  exit 1
fi

REGISTER_CHECKER=0

while getopts "n:l:rh" option
    do
    case "${option}"
    in
    n) NAME_OF_CHECKER=${OPTARG};;
    l) LOCATION=${OPTARG};;
    r) REGISTER_CHECKER=1;;
    h | *) usage; exit 0;;
    esac
done

if [ -z "${NAME_OF_CHECKER+x}" ]; then
  usage
  exit 0
fi

LOCATION=${LOCATION:-"${DIR}/checker"}

echo "INFO: Creating new checker with name '${NAME_OF_CHECKER}' in '${LOCATION}'"

# TODO Implement
