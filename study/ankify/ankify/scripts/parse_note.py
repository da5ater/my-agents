#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


H2_RE = re.compile(r"^##\s+(.*)$")
H3_RE = re.compile(r"^###\s+(.*)$")
CODE_FENCE_RE = re.compile(r"^```")

MENTAL_MODEL_PHRASES = ["how it works", "architecture", "flow", "lifecycle"]
FAILURE_TRIGGER_PHRASES = ["common mistake", "pitfall", "warning", "gotcha", "avoid"]
CONTRADICTION_PHRASES = [
    "contradiction",
    "counter-evidence",
    "counter evidence",
    "disprove",
]
DISTINCTION_PHRASES = ["distinction", "negation", "differs from"]


def load_lexicon(script_path):
    lexicon_path = Path(script_path).parent / "lexicon.json"
    if not lexicon_path.exists():
        return {}
    try:
        with open(lexicon_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}


def normalize_title(title):
    return re.sub(r"\s+", " ", title.strip())


def main():
    parser = argparse.ArgumentParser(
        description="Parse an Obsidian note for structural metadata."
    )
    parser.add_argument("--input", required=True, help="Path to markdown note.")
    parser.add_argument(
        "--output", required=True, help="Path to write parsed metadata JSON."
    )
    args = parser.parse_args()

    lexicon = load_lexicon(__file__)

    mental_phrases = lexicon.get("mental_model_phrases", MENTAL_MODEL_PHRASES)
    failure_phrases = lexicon.get("failure_trigger_phrases", FAILURE_TRIGGER_PHRASES)
    contradiction_phrases = lexicon.get("contradiction_phrases", CONTRADICTION_PHRASES)
    distinction_phrases = lexicon.get("distinction_phrases", DISTINCTION_PHRASES)

    with open(args.input, "r", encoding="utf-8") as handle:
        lines = handle.readlines()

    h2_titles = []
    h3_titles = []
    code_blocks = 0
    in_code_block = False

    mental_models_present = False
    failure_mode_triggers_present = False
    contradictions_present = False
    distinctions_present = False

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        if CODE_FENCE_RE.match(line):
            in_code_block = not in_code_block
            if in_code_block:
                code_blocks += 1
            continue

        if in_code_block:
            continue

        h2_match = H2_RE.match(line)
        if h2_match:
            h2_titles.append(normalize_title(h2_match.group(1)))
            continue

        h3_match = H3_RE.match(line)
        if h3_match:
            h3_title = normalize_title(h3_match.group(1))
            h3_titles.append(h3_title)
            lower = h3_title.lower()
            if "mental model" in lower:
                mental_models_present = True
            if "counter-evidence" in lower or "counter evidence" in lower:
                contradictions_present = True
            if "distinctions" in lower or "negations" in lower:
                distinctions_present = True
            if "common mistake" in lower:
                failure_mode_triggers_present = True
            continue

        lower_line = line.lower()
        if any(phrase in lower_line for phrase in mental_phrases):
            mental_models_present = True
        if any(phrase in lower_line for phrase in failure_phrases):
            failure_mode_triggers_present = True
        if any(phrase in lower_line for phrase in contradiction_phrases):
            contradictions_present = True
        if any(phrase in lower_line for phrase in distinction_phrases):
            distinctions_present = True

    metadata = {
        "concept_count": len(h2_titles),
        "h2_count": len(h2_titles),
        "h3_count": len(h3_titles),
        "h2_titles": h2_titles,
        "h3_titles": h3_titles,
        "code_blocks": code_blocks,
        "structural_elements": len(h2_titles) + len(h3_titles) + code_blocks,
        "mental_models_present": mental_models_present,
        "failure_mode_triggers_present": failure_mode_triggers_present,
        "contradictions_present": contradictions_present,
        "distinctions_present": distinctions_present,
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
