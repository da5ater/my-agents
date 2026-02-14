#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: validate_tsv.sh <tsv_file>" >&2
  exit 2
fi

INPUT_FILE="$1"

awk -F'\t' '{
  if (NF != 3) print "FAIL line " NR ": " NF " columns (expected 3)"
  if ($1 ~ /\[Source:/) print "FAIL line " NR ": [Source:] in FRONT column"
  if ($1 ~ /\t/ || $2 ~ /\t/) print "FAIL line " NR ": literal tab in content"
}' "$INPUT_FILE"
