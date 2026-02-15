#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: run_ankify_checks_loop.sh <note.md> <output.tsv> [run_stats.json]" >&2
  exit 2
fi

NOTE_PATH="$1"
TSV_PATH="$2"
RUN_STATS_PATH="${3:-}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MAX_ITER="${MAX_ITER:-5}"
REGEN_CMD="${REGEN_CMD:-}"
VAULT_NAME="${VAULT_NAME:-mohamed}"
VAULT_ROOT="${VAULT_ROOT:-/mnt/data/obsidian/mohamed}"

DOCTRINE_REPORT="${NOTE_PATH}.doctrine_report.json"
PRUNE_PLAN="${NOTE_PATH}.prune_plan.json"
CONVERSION_PLAN="${NOTE_PATH}.conversion_plan.json"
NOTE_META="${NOTE_PATH}.meta.json"
CONVERSION_AUDIT="${NOTE_PATH}.conversion_audit.json"
AUDIT_SUMMARY="${NOTE_PATH}.audit_summary.txt"
POST_VALIDATE_REPORT="${NOTE_PATH}.post_validate.txt"
CAP_PRUNE_PLAN="${NOTE_PATH}.cap_prune_plan.json"
CARDS_JSON="${NOTE_PATH}.cards.json"
CARD_BUDGET="${NOTE_PATH}.card_budget.json"

iter=1
while [ "$iter" -le "$MAX_ITER" ]; do
  "${SCRIPT_DIR}/run_ankify_checks.sh" "$NOTE_PATH" "$TSV_PATH" "$RUN_STATS_PATH"

  if "${SCRIPT_DIR}/check_ankify_reports.py" --doctrine "$DOCTRINE_REPORT" --prune "$PRUNE_PLAN"; then
    "${SCRIPT_DIR}/summarize_ankify_audit.py" --doctrine "$DOCTRINE_REPORT" --prune "$PRUNE_PLAN" --conversion "$CONVERSION_AUDIT" --cap-prune "$CAP_PRUNE_PLAN" --output "$AUDIT_SUMMARY"
    exit 0
  fi

  if [ -n "$REGEN_CMD" ]; then
    eval "$REGEN_CMD"
  else
    "${SCRIPT_DIR}/apply_conversion.py" --tsv "$TSV_PATH" --conversion "$CONVERSION_PLAN" --note-meta "$NOTE_META" --budget "$CARD_BUDGET" --output "$TSV_PATH" --audit "$CONVERSION_AUDIT"
    "${SCRIPT_DIR}/apply_prune.py" --tsv "$TSV_PATH" --prune "$PRUNE_PLAN" --output "$TSV_PATH"
    "${SCRIPT_DIR}/cap_prune.py" --cards "$CARDS_JSON" --budget "$CARD_BUDGET" --output "$CAP_PRUNE_PLAN"
    "${SCRIPT_DIR}/apply_prune.py" --tsv "$TSV_PATH" --prune "$CAP_PRUNE_PLAN" --output "$TSV_PATH"
    "${SCRIPT_DIR}/append_missing_types.py" --tsv "$TSV_PATH" --doctrine "$DOCTRINE_REPORT" --note-meta "$NOTE_META" --note-path "$NOTE_PATH" --vault "$VAULT_NAME" --vault-root "$VAULT_ROOT" --budget "$CARD_BUDGET"
    "${SCRIPT_DIR}/validate_tsv.sh" "$TSV_PATH" > "$POST_VALIDATE_REPORT" || true
    if [ -s "$POST_VALIDATE_REPORT" ]; then
      exit 1
    fi
  fi
  iter=$((iter + 1))
done

"${SCRIPT_DIR}/summarize_ankify_audit.py" --doctrine "$DOCTRINE_REPORT" --prune "$PRUNE_PLAN" --conversion "$CONVERSION_AUDIT" --cap-prune "$CAP_PRUNE_PLAN" --output "$AUDIT_SUMMARY"
exit 0
