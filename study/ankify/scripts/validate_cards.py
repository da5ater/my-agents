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

BANNED_FRONT_PATTERNS = [
    re.compile(r"write the code example for", re.IGNORECASE),
    re.compile(r"write a minimal variant", re.IGNORECASE),
    re.compile(r"what goes wrong if .* is misused", re.IGNORECASE),
    re.compile(r"what is .* not\?", re.IGNORECASE),
]

BANNED_BACK_PHRASES = [
    "leads to incorrect behavior",
    "focuses on its own role",
    "not just a synonym",
]

YES_NO_PREFIXES = [
    "is ",
    "are ",
    "do ",
    "does ",
    "can ",
    "should ",
    "will ",
    "did ",
]

MISUSE_VERBS = [
    "mutate",
    "reassign",
    "call",
    "pass",
    "use",
    "set",
    "assign",
    "splice",
    "push",
    "pop",
    "shift",
    "unshift",
    "sort",
    "reverse",
    "compare",
    "coerce",
    "update",
    "modify",
]

ALIGNMENT_TRIGGERS = [
    "compare",
    "differ from",
    "explain/visualize",
]

DIMENSION_KEYWORDS = [
    "mutation",
    "return value",
    "time complexity",
    "space complexity",
    "side effects",
    "ordering",
    "typical use",
]

STOPWORDS = {
    "const",
    "let",
    "var",
    "function",
    "return",
    "class",
    "new",
    "this",
    "super",
    "if",
    "else",
    "for",
    "while",
    "switch",
    "case",
    "break",
    "default",
    "true",
    "false",
    "null",
    "undefined",
}

STAGE_MARKERS = ["1)", "2)", "first", "second", "then", "next", "finally", "stage"]
FAILURE_MARKERS = ["if", "when"]
COUNTER_MARKERS = ["when", "unless", "except", "if"]

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


def extract_keywords(text):
    tokens = re.findall(r"[A-Za-z_][A-Za-z0-9_]+", text)
    keywords = []
    seen = set()
    for token in tokens:
        lower = token.lower()
        if lower in STOPWORDS:
            continue
        if len(lower) < 4:
            continue
        if lower in seen:
            continue
        seen.add(lower)
        keywords.append(lower)
    return keywords[:20]


def has_keyword(text, keywords):
    lower = text.lower()
    return any(k in lower for k in keywords)


def count_markers(text, markers):
    lower = text.lower()
    return sum(1 for marker in markers if marker in lower)


def count_anchor_hits(text, anchors):
    lower = text.lower()
    matched = set()
    for anchor in anchors:
        if not anchor:
            continue
        token = anchor.lower()
        if re.search(r"\b" + re.escape(token) + r"\b", lower):
            matched.add(token)
    return len(matched)


def has_bullets(text):
    return re.search(r"(^|<br>)\s*[-*]\s+", text) is not None


def has_step_sequence(text):
    return (
        re.search(r"\b1\)|\b1\.\s", text) is not None
        and re.search(r"\b2\)|\b2\.\s", text) is not None
    )


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
    keywords = []
    anchors = []
    note_path = ""
    if args.note_metadata:
        with open(args.note_metadata, "r", encoding="utf-8") as handle:
            note_meta = json.load(handle)
        concepts = note_meta.get("h2_titles", [])
        note_path = note_meta.get("note_path", "")
        anchor_meta = note_meta.get("anchors", {})
        if isinstance(anchor_meta, dict):
            anchors.extend(anchor_meta.get("methods", []))
            anchors.extend(anchor_meta.get("keywords", []))
        anchors = [a for a in anchors if a]
        if note_path:
            try:
                with open(note_path, "r", encoding="utf-8") as handle:
                    note_text = handle.read()
                keywords = extract_keywords(note_text)
            except OSError:
                keywords = []

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

    generic_failures = []
    quality_failures = []
    manifesto_failures = []
    manifesto_samples = {
        "MC-CTX-001": [],
        "MC-WHITEBOARD-001": [],
        "MC-INTERVIEW-001": [],
        "MC-SIGNAL-001": [],
    }
    banned_pattern_hits = {pattern.pattern: 0 for pattern in BANNED_FRONT_PATTERNS}
    for phrase in BANNED_BACK_PHRASES:
        banned_pattern_hits[phrase] = 0
    banned_pattern_hits["key parts"] = 0
    output_purity_ok = True

    with open(args.tsv, "r", encoding="utf-8") as handle:
        for line_index, raw_line in enumerate(handle):
            if not raw_line.endswith("\n"):
                output_purity_ok = False
            line = raw_line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                output_purity_ok = False
                continue
            front, back, _ = parts
            if any("\t" in part for part in parts):
                output_purity_ok = False
            counts["total_cards"] += 1

            question_text = strip_html(extract_question_text(front))
            question_lower = question_text.lower()
            back_text = strip_html(back)
            back_lower = back_text.lower().strip()
            card_id = f"{note_path}#{line_index}" if note_path else f"line#{line_index}"

            for pattern in BANNED_FRONT_PATTERNS:
                if pattern.search(question_text):
                    banned_pattern_hits[pattern.pattern] += 1
                    quality_failures.append("banned_front")
                    manifesto_failures.append("MC-SIGNAL-001")

            for phrase in BANNED_BACK_PHRASES:
                if phrase in back_lower:
                    banned_pattern_hits[phrase] += 1
                    quality_failures.append("banned_back")
                    manifesto_failures.append("MC-SIGNAL-001")

            if back_lower.startswith("key parts:"):
                banned_pattern_hits["key parts"] += 1
                quality_failures.append("banned_back")
                manifesto_failures.append("MC-SIGNAL-001")

            interview_ok = True
            if any(question_lower.startswith(prefix) for prefix in YES_NO_PREFIXES):
                quality_failures.append("yes_no_prompt")
                manifesto_failures.append("MC-INTERVIEW-001")
                interview_ok = False

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

            if any(phrase.lower() in question_lower for phrase in failure_phrases):
                counts["failure_mode_cards"] += 1

            topic = extract_topic(front)
            if concepts:
                ref_count = count_concept_refs(question_text, concepts)
                if ref_count >= 2 and contains_relational_operator(
                    question_text, operators
                ):
                    counts["cross_h2_synthesis_cards"] += 1
                if ref_count >= 1 and (
                    not topic or topic.lower() not in question_lower
                ):
                    counts["connectivity_cards"] += 1

            ctx_ok = True
            whiteboard_ok = True
            signal_ok = True

            if card_type == "CONSTRUCTIVE":
                if "given:" not in question_lower or "task:" not in question_lower:
                    ctx_ok = False
                    whiteboard_ok = False
                task_text = ""
                task_match = re.search(r"task:\s*(.*)$", question_text, re.IGNORECASE)
                if task_match:
                    task_text = task_match.group(1).strip().lower()
                if not task_text:
                    whiteboard_ok = False
                if " and " in task_text or " or " in task_text:
                    whiteboard_ok = False
                if "line" not in task_text:
                    whiteboard_ok = False
                if count_anchor_hits(question_text, anchors) < 1:
                    ctx_ok = False
                if "<pre" in back and "<code>" in back:
                    code_lines = back.count("<br>") + 1
                    if code_lines > 2:
                        whiteboard_ok = False
                if not ctx_ok:
                    quality_failures.append("context_mandate")
                    manifesto_failures.append("MC-CTX-001")
                if not whiteboard_ok:
                    quality_failures.append("whiteboard_rule")
                    manifesto_failures.append("MC-WHITEBOARD-001")
                if (
                    ctx_ok
                    and card_id not in manifesto_samples["MC-CTX-001"]
                    and len(manifesto_samples["MC-CTX-001"]) < 3
                ):
                    manifesto_samples["MC-CTX-001"].append(card_id)
                if (
                    whiteboard_ok
                    and card_id not in manifesto_samples["MC-WHITEBOARD-001"]
                    and len(manifesto_samples["MC-WHITEBOARD-001"]) < 3
                ):
                    manifesto_samples["MC-WHITEBOARD-001"].append(card_id)

            if card_type in {
                "MODEL",
                "FAILURE_MODE",
                "COUNTER_EVIDENCE",
                "NEGATION",
                "SYNTHESIS",
            }:
                if count_anchor_hits(question_text, anchors) < 1:
                    quality_failures.append("missing_anchor")
                    signal_ok = False

            if card_type == "FAILURE_MODE":
                if "misused" in question_lower:
                    quality_failures.append("failure_mode_generic")
                    signal_ok = False
                if not any(verb in question_lower for verb in MISUSE_VERBS):
                    quality_failures.append("failure_mode_missing_action")
                    signal_ok = False
                if count_anchor_hits(question_text, anchors) < 1:
                    quality_failures.append("failure_mode_missing_anchor")
                    signal_ok = False
                if not any(
                    marker in back_lower
                    for marker in [
                        "then",
                        "so",
                        "therefore",
                        "consequence",
                        "results",
                        "leads",
                        "causes",
                        "throws",
                        "breaks",
                    ]
                ):
                    quality_failures.append("failure_mode_missing_consequence")
                    signal_ok = False

            if card_type == "COUNTER_EVIDENCE":
                if (
                    "when does" not in question_lower
                    or "not apply" not in question_lower
                ):
                    quality_failures.append("counter_evidence_open")
                    signal_ok = False
                if count_anchor_hits(question_text, anchors) < 1:
                    quality_failures.append("counter_evidence_missing_anchor")
                    signal_ok = False
                if (
                    count_anchor_hits(back_text, anchors) < 1
                    and "example" not in back_lower
                ):
                    quality_failures.append("counter_evidence_missing_example")
                    signal_ok = False

            if card_type == "NEGATION":
                if (
                    not question_lower.startswith("how does")
                    or "differ from" not in question_lower
                ):
                    quality_failures.append("negation_open")
                    signal_ok = False
                if count_anchor_hits(question_text, anchors) < 2:
                    quality_failures.append("negation_missing_anchors")
                    signal_ok = False
                if sum(1 for kw in DIMENSION_KEYWORDS if kw in back_lower) < 2:
                    quality_failures.append("negation_missing_dimensions")
                    signal_ok = False

            if card_type == "SYNTHESIS":
                if "compare" not in question_lower:
                    quality_failures.append("synthesis_open")
                    signal_ok = False
                if count_anchor_hits(question_text, anchors) < 2:
                    quality_failures.append("synthesis_missing_anchors")
                    signal_ok = False
                if sum(1 for kw in DIMENSION_KEYWORDS if kw in back_lower) < 2:
                    quality_failures.append("synthesis_missing_dimensions")
                    signal_ok = False

            if any(trigger in question_lower for trigger in ALIGNMENT_TRIGGERS):
                if not (
                    count_anchor_hits(back_text, anchors) >= 2
                    or has_bullets(back)
                    or has_step_sequence(back)
                ):
                    quality_failures.append("qa_alignment")
                    signal_ok = False

            if not signal_ok:
                manifesto_failures.append("MC-SIGNAL-001")
            if (
                signal_ok
                and card_id not in manifesto_samples["MC-SIGNAL-001"]
                and len(manifesto_samples["MC-SIGNAL-001"]) < 3
            ):
                manifesto_samples["MC-SIGNAL-001"].append(card_id)
            if (
                interview_ok
                and card_id not in manifesto_samples["MC-INTERVIEW-001"]
                and len(manifesto_samples["MC-INTERVIEW-001"]) < 3
            ):
                manifesto_samples["MC-INTERVIEW-001"].append(card_id)

            if card_type in {"MODEL", "FAILURE_MODE", "COUNTER_EVIDENCE", "SYNTHESIS"}:
                if keywords:
                    if card_type == "MODEL":
                        if count_markers(back, STAGE_MARKERS) < 2 or not has_keyword(
                            back, keywords
                        ):
                            generic_failures.append("model_generic")
                    if card_type == "FAILURE_MODE":
                        if count_markers(back, FAILURE_MARKERS) < 1 or not has_keyword(
                            back, keywords
                        ):
                            generic_failures.append("failure_mode_generic")
                    if card_type == "COUNTER_EVIDENCE":
                        if count_markers(back, COUNTER_MARKERS) < 1 or not has_keyword(
                            back, keywords
                        ):
                            generic_failures.append("counter_evidence_generic")
                    if card_type == "SYNTHESIS":
                        if not references_two_distinct_concepts(
                            question_text, concepts
                        ):
                            generic_failures.append("synthesis_generic")

    quality_ok = True
    if (
        generic_failures
        or quality_failures
        or manifesto_failures
        or not output_purity_ok
    ):
        quality_ok = False

    output = {}
    output.update(note_meta)
    output.update(counts)
    output["quality_ok"] = quality_ok
    output["output_purity_ok"] = output_purity_ok
    if generic_failures:
        output["generic_failures"] = sorted(set(generic_failures))
    if quality_failures:
        output["quality_failures"] = sorted(set(quality_failures))
    if manifesto_failures:
        output["manifesto_failures"] = sorted(set(manifesto_failures))
    output["manifesto_samples"] = manifesto_samples
    output["banned_pattern_hits"] = banned_pattern_hits

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
