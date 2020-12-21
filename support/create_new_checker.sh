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

if [[ "${NAME_OF_CHECKER}" != samo_* || "${NAME_OF_CHECKER}" != *_checker || "${NAME_OF_CHECKER}" == *-* ]]; then
  echo "ERROR: Name of the checker shall start with 'samo', end with 'checker' and not contains any '-'"
  exit 1
fi

LOCATION=${LOCATION:-"${DIR}/../samo_tidy/checker"}

if [[ ! -d "${LOCATION}" || ! -d "${LOCATION}/test" || ! -d "${LOCATION}/test/data" ]]; then
  echo "ERROR: One of '${LOCATION}', '${LOCATION}/test' or '${LOCATION}/test/data' does not exist"
  exit 1
fi

NAME_CAMEL_CASE=$(echo "${NAME_OF_CHECKER}" | perl -pe 's/(^|_)([a-z])/uc($2)/ge')
NAME_UPPER_CASE=$(echo "${NAME_OF_CHECKER}" | tr a-z A-Z)

echo "INFO: Checker name (snake_case): ${NAME_OF_CHECKER}"
echo "INFO: Checker name (CamelCase): ${NAME_CAMEL_CASE}"
echo "INFO: Checker name (UPPER_CASE): ${NAME_UPPER_CASE}"

CHECKER_FILE_LOCATION="${LOCATION}/${NAME_OF_CHECKER}.py"
CHECKER_TEST_FILE_LOCATION="${LOCATION}/test/test_${NAME_OF_CHECKER}.py"
CHECKER_TEST_SOURCE_FILE_LOCATION="${LOCATION}/test/data/${NAME_OF_CHECKER}.cpp"

echo "INFO: Creating new checker file in '${CHECKER_FILE_LOCATION}'"
cp "${DIR}/templates/samo_tidy_template_checker.py" "${CHECKER_FILE_LOCATION}"

echo "INFO: Creating new checker test file in '${CHECKER_TEST_FILE_LOCATION}'"
cp "${DIR}/templates/test_samo_tidy_template_checker.py" "${CHECKER_TEST_FILE_LOCATION}"

echo "INFO: Creating new checker test source file in '${CHECKER_TEST_SOURCE_FILE_LOCATION}'"
cp "${DIR}/templates/samo_tidy_template_checker.cpp" "${CHECKER_TEST_SOURCE_FILE_LOCATION}"


function replace {
    sed -i '' "s/@TIDY_NAME/${NAME_OF_CHECKER}/g" "${1}"
    sed -i '' "s/@TIDY_ID/${NAME_UPPER_CASE}/g" "${1}"
    sed -i '' "s/@TIDY_CAMEL_CASE/${NAME_CAMEL_CASE}/g" "${1}"
    sed -i '' "s/@TIDY_MESSAGE/Violation of ${NAME_UPPER_CASE}/g" "${1}"
}

replace "${CHECKER_FILE_LOCATION}"
replace "${CHECKER_TEST_FILE_LOCATION}"
replace "${CHECKER_TEST_SOURCE_FILE_LOCATION}"
