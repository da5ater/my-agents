#!/usr/bin/env python3
import argparse
import json
import math
import re
import sys
from pathlib import Path


RELATIONAL_OPERATORS = [
    "compare",
    "differ",
    "tradeoff",
    "impact",
    "influence",
    "interact",
    "dependency",
    "contrast",
    "affects",
]

ACTIVE_RECALL_VERBS = [
    "Write",
    "Explain",
    "Describe",
    "Implement",
    "Build",
    "Create",
    "Add",
]

MODEL_PHRASES = ["Explain/visualize how", "What are the stages"]
FAILURE_MODE_PHRASES = ["What goes wrong", "breaks if"]
NEGATION_PHRASES = ["NOT", "differs from"]
COUNTER_EVIDENCE_PHRASES = ["What contradicts", "NOT apply"]

TYPE_NORMALIZATION = {
    "COUNTER-EVIDENCE": "COUNTER_EVIDENCE",
    "COUNTER EVIDENCE": "COUNTER_EVIDENCE",
    "FAILURE MODE": "FAILURE_MODE",
    "FAILURE-MODE": "FAILURE_MODE",
    "NEGATION": "NEGATION",
    "MODEL": "MODEL",
    "SYNTHESIS": "SYNTHESIS",
    "CONSTRUCTIVE": "CONSTRUCTIVE",
    "THEORY": "THEORY",
    "DEFINITION": "DEFINITION",
    "PROCEDURE": "PROCEDURE",
}


def load_lexicon(script_path):
    lexicon_path = Path(script_path).parent / "lexicon.json"
    if not lexicon_path.exists():
        return {}
    try:
        with open(lexicon_path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return {}


def extract_topic(front):
    match = re.search(r"<strong>(.*?)</strong>", front)
    if not match:
        return ""
    return match.group(1).strip()


def tokenize(text):
    return re.findall(r"[A-Za-z0-9_]+", text.lower())


def contains_relational_operator(text, operators):
    lower = text.lower()
    return any(op in lower for op in operators)


def references_two_distinct_concepts(text, concepts):
    lower = text.lower()
    matched = []
    for concept in concepts:
        if concept and concept.lower() in lower:
            matched.append(concept)
    distinct = list(dict.fromkeys(matched))
    return len(distinct) >= 2


def count_concept_refs(text, concepts):
    lower = text.lower()
    count = 0
    for concept in concepts:
        if concept and concept.lower() in lower:
            count += 1
    return count


def classify_card(
    question_text,
    back,
    concepts,
    operators,
    verbs,
    model_phrases,
    negation_phrases,
    counter_phrases,
):
    if "<pre" in back and "<code>" in back:
        return "CONSTRUCTIVE"
    if any(phrase.lower() in question_text.lower() for phrase in counter_phrases):
        return "COUNTER_EVIDENCE"
    if any(phrase.lower() in question_text.lower() for phrase in negation_phrases):
        return "NEGATION"
    if any(phrase.lower() in question_text.lower() for phrase in model_phrases):
        return "MODEL"
    if question_text.lower().startswith("what is "):
        return "DEFINITION"
    if question_text.lower().startswith(
        "how do you"
    ) or question_text.lower().startswith("how to"):
        return "PROCEDURE"
    if contains_relational_operator(
        question_text, operators
    ) and references_two_distinct_concepts(question_text, concepts):
        return "SYNTHESIS"
    if any(question_text.lower().startswith(verb.lower()) for verb in verbs):
        return "THEORY"
    return "THEORY"


def extract_question_text(front):
    split_token = "</strong><br>"
    if split_token in front:
        return front.split(split_token, 1)[1]
    return front


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


def normalize_type_label(text):
    upper = text.upper()
    for key, value in TYPE_NORMALIZATION.items():
        if key in upper:
            return value
    return ""


def main():
    parser = argparse.ArgumentParser(
        description="Validate cards and compute counts from TSV."
    )
    parser.add_argument("--tsv", required=True, help="Path to TSV output.")
    parser.add_argument(
        "--note-metadata", required=False, help="Path to parse_note.py output JSON."
    )
    parser.add_argument("--output", required=True, help="Path to write raw stats JSON.")
    args = parser.parse_args()

    lexicon = load_lexicon(__file__)

    operators = lexicon.get("relational_operators", RELATIONAL_OPERATORS)
    verbs = lexicon.get("active_recall_verbs", ACTIVE_RECALL_VERBS)
    model_phrases = lexicon.get("model_phrases", MODEL_PHRASES)
    failure_phrases = lexicon.get("failure_mode_phrases", FAILURE_MODE_PHRASES)
    negation_phrases = lexicon.get("negation_phrases", NEGATION_PHRASES)
    counter_phrases = lexicon.get("counter_evidence_phrases", COUNTER_EVIDENCE_PHRASES)

    concepts = []
    note_meta = {}
    if args.note_metadata:
        with open(args.note_metadata, "r", encoding="utf-8") as handle:
            note_meta = json.load(handle)
        concepts = note_meta.get("h2_titles", [])

    counts = {
        "total_cards": 0,
        "synthesis_cards": 0,
        "cross_h2_synthesis_cards": 0,
        "model_cards": 0,
        "failure_mode_cards": 0,
        "negation_cards": 0,
        "counter_evidence_cards": 0,
        "connectivity_cards": 0,
        "definition_cards": 0,
        "procedure_cards": 0,
        "constructive_cards": 0,
        "theory_cards": 0,
    }

    with open(args.tsv, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            front, back, _ = parts
            counts["total_cards"] += 1

            question_text = strip_html(extract_question_text(front))
            normalized = normalize_type_label(front)
            if normalized:
                card_type = normalized
            else:
                card_type = classify_card(
                    question_text,
                    back,
                    concepts,
                    operators,
                    verbs,
                    model_phrases,
                    negation_phrases,
                    counter_phrases,
                )
            if card_type == "CONSTRUCTIVE":
                counts["constructive_cards"] += 1
            if card_type == "THEORY":
                counts["theory_cards"] += 1
            if card_type == "SYNTHESIS":
                counts["synthesis_cards"] += 1
            if card_type == "MODEL":
                counts["model_cards"] += 1
            if card_type == "NEGATION":
                counts["negation_cards"] += 1
            if card_type == "COUNTER_EVIDENCE":
                counts["counter_evidence_cards"] += 1
            if card_type == "DEFINITION":
                counts["definition_cards"] += 1
            if card_type == "PROCEDURE":
                counts["procedure_cards"] += 1

            if any(
                phrase.lower() in question_text.lower() for phrase in failure_phrases
            ):
                counts["failure_mode_cards"] += 1

            topic = extract_topic(front)
            if concepts:
                ref_count = count_concept_refs(question_text, concepts)
                if ref_count >= 2 and contains_relational_operator(
                    question_text, operators
                ):
                    counts["cross_h2_synthesis_cards"] += 1
                if ref_count >= 1 and (
                    not topic or topic.lower() not in question_text.lower()
                ):
                    counts["connectivity_cards"] += 1

    output = {}
    output.update(note_meta)
    output.update(counts)

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
