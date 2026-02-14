#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: run_ankify_checks.sh <note.md> <output.tsv> [run_stats.json]" >&2
  exit 2
fi

NOTE_PATH="$1"
TSV_PATH="$2"
RUN_STATS_PATH="${3:-}"
REQUIRE_RUN_STATS="${REQUIRE_RUN_STATS:-0}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

NOTE_META="${NOTE_PATH}.meta.json"
RAW_STATS="${NOTE_PATH}.raw_stats.json"
COUNTS="${NOTE_PATH}.counts.json"
CARD_BUDGET="${NOTE_PATH}.card_budget.json"
DOCTRINE_REPORT="${NOTE_PATH}.doctrine_report.json"

"${SCRIPT_DIR}/parse_note.py" --input "$NOTE_PATH" --output "$NOTE_META"
"${SCRIPT_DIR}/compute_card_budget_pre.py" --note-meta "$NOTE_META" --output "$CARD_BUDGET"
"${SCRIPT_DIR}/validate_cards.py" --tsv "$TSV_PATH" --note-metadata "$NOTE_META" --output "$RAW_STATS"
"${SCRIPT_DIR}/build_counts.py" --input "$RAW_STATS" --output "$COUNTS"

if [ -n "$RUN_STATS_PATH" ]; then
  "${SCRIPT_DIR}/compute_doctrine_report.py" --counts "$COUNTS" --budget "$CARD_BUDGET" --run-stats "$RUN_STATS_PATH" > "$DOCTRINE_REPORT"
else
  if [ "$REQUIRE_RUN_STATS" = "1" ]; then
    "${SCRIPT_DIR}/compute_doctrine_report.py" --counts "$COUNTS" --budget "$CARD_BUDGET" --require-run-stats > "$DOCTRINE_REPORT"
  else
    "${SCRIPT_DIR}/compute_doctrine_report.py" --counts "$COUNTS" --budget "$CARD_BUDGET" > "$DOCTRINE_REPORT"
  fi
fi

echo "Wrote:" >&2
echo "$NOTE_META" >&2
echo "$CARD_BUDGET" >&2
echo "$RAW_STATS" >&2
echo "$COUNTS" >&2
echo "$DOCTRINE_REPORT" >&2
