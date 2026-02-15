#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


H2_RE = re.compile(r"^##\s+(.*)$")
H3_RE = re.compile(r"^###\s+(.*)$")
CODE_FENCE_RE = re.compile(r"^```")
ORDERED_STEP_RE = re.compile(r"^\s*\d+\.")
METHOD_CALL_RE = re.compile(r"\.([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")
ANCHOR_KEYWORDS = [
    "const",
    "let",
    "var",
    "this",
    "new",
    "class",
    "prototype",
    "arguments",
    "async",
    "await",
    "yield",
    "return",
    "try",
    "catch",
    "finally",
    "throw",
    "import",
    "export",
]

MENTAL_MODEL_PHRASES = [
    "how it works",
    "architecture",
    "flow",
    "end-to-end",
    "stages",
    "sequence",
    "process",
    "workflow",
    "state machine",
    "state transition",
    "lifecycle",
    "pipeline",
    "data flow",
    "control flow",
    "request flow",
    "execution path",
]
FAILURE_TRIGGER_PHRASES = [
    "common mistake",
    "pitfall",
    "warning",
    "gotcha",
    "avoid",
    "edge case",
    "breaks if",
    "fails if",
    "failure mode",
    "error",
    "exception",
    "undefined behavior",
    "bug",
    "caution",
    "danger",
]
CONTRADICTION_PHRASES = [
    "contradiction",
    "counter-evidence",
    "counter evidence",
    "disprove",
    "counterexample",
    "exception",
    "unless",
    "except",
    "not apply",
    "does not apply",
    "fails when",
]
DISTINCTION_PHRASES = [
    "distinction",
    "negation",
    "differs from",
    "vs",
    "versus",
    "unlike",
    "different from",
    "not the same",
    "tradeoff",
    "contrast",
]


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


def phrase_matches(phrase, text):
    if len(phrase) <= 3:
        return re.search(r"\b" + re.escape(phrase) + r"\b", text) is not None
    return phrase in text


def add_unique(items, value):
    if value in items:
        return
    items.append(value)


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
    ordered_step_count = 0

    anchor_methods = []
    anchor_keywords = []

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
            for method in METHOD_CALL_RE.findall(line):
                add_unique(anchor_methods, method)
            lower_line = line.lower()
            for keyword_token in ANCHOR_KEYWORDS:
                if re.search(r"\b" + re.escape(keyword_token) + r"\b", lower_line):
                    add_unique(anchor_keywords, keyword_token)
            continue

        h2_match = H2_RE.match(line)
        if h2_match:
            title = normalize_title(h2_match.group(1))
            h2_titles.append(title)
            lower_title = title.lower()
            if any(phrase_matches(phrase, lower_title) for phrase in mental_phrases):
                mental_models_present = True
            if any(phrase_matches(phrase, lower_title) for phrase in failure_phrases):
                failure_mode_triggers_present = True
            if any(
                phrase_matches(phrase, lower_title) for phrase in contradiction_phrases
            ):
                contradictions_present = True
            if any(
                phrase_matches(phrase, lower_title) for phrase in distinction_phrases
            ):
                distinctions_present = True
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
            if any(phrase_matches(phrase, lower) for phrase in mental_phrases):
                mental_models_present = True
            if any(phrase_matches(phrase, lower) for phrase in failure_phrases):
                failure_mode_triggers_present = True
            if any(phrase_matches(phrase, lower) for phrase in contradiction_phrases):
                contradictions_present = True
            if any(phrase_matches(phrase, lower) for phrase in distinction_phrases):
                distinctions_present = True
            continue

        lower_line = line.lower()
        if ORDERED_STEP_RE.match(line):
            ordered_step_count += 1
            if ordered_step_count >= 2:
                mental_models_present = True
        if any(phrase_matches(phrase, lower_line) for phrase in mental_phrases):
            mental_models_present = True
        if any(phrase_matches(phrase, lower_line) for phrase in failure_phrases):
            failure_mode_triggers_present = True
        if any(phrase_matches(phrase, lower_line) for phrase in contradiction_phrases):
            contradictions_present = True
        if any(phrase_matches(phrase, lower_line) for phrase in distinction_phrases):
            distinctions_present = True

    metadata = {
        "note_path": str(Path(args.input).resolve()),
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
        "anchors": {
            "methods": anchor_methods,
            "keywords": anchor_keywords,
        },
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
