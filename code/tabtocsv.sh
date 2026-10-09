#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "error: input exactly one argument." >&2
  exit 2
fi

if [[ ! -f "$1" || ! -r "$1" ]]; then
  echo "error: $1 doesn't exist or is not readable" >&2
  exit 1
fi

echo "Creating a comma delimited version of $1 ..."
input_name=$(basename "$1")
output_file="../results/${input_name}.csv"

if ! mkdir -p ../results; then
  echo "Cannot create the results directory." >&2
  exit 1
fi

if ! tr '\t' ',' < "$1" > "$output_file"; then
  echo "Error occurred while converting tabs to commas." >&2
  exit 1
fi

echo "Done!"
exit 0