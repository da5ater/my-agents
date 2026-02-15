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
  if ($1 !~ /^<strong>.*<\/strong><br>/) print "FAIL line " NR ": invalid FRONT format"
  if ($3 !~ /^obsidian:\/\/open\?vault=mohamed&file=/) print "FAIL line " NR ": invalid Obsidian URL"
  split($3, a, "file=")
  path=a[2]
  if (path ~ /\.md$/) print "FAIL line " NR ": .md suffix in URL"
  if (path ~ /\//) print "FAIL line " NR ": unencoded slash in URL"
  if (path ~ / /) print "FAIL line " NR ": space not URL-encoded"
}' "$INPUT_FILE"
