#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys


def encode_obsidian_url(vault, path):
    rel = path.replace(".md", "")
    rel = rel.replace("/", "%2F").replace(" ", "%20")
    return f"obsidian://open?vault={vault}&file={rel}"


CODE_FENCE_RE = re.compile(r"^```")


def strip_markdown(text):
    text = re.sub(r"^>+\s*", "", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text)
    text = re.sub(r"^\s*\d+\.\s+", "", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"!\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def sanitize_field(text):
    text = text.replace("\t", " ")
    text = text.replace("\n", "<br>")
    return text


def extract_content_lines(note_lines):
    content = []
    in_code = False
    for raw in note_lines:
        line = raw.rstrip("\n")
        if CODE_FENCE_RE.match(line):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not line.strip():
            continue
        if line.lstrip().startswith("#"):
            continue
        if line.lstrip().startswith(">"):
            continue
        cleaned = strip_markdown(line)
        if cleaned:
            content.append(cleaned)
    return content


def tokenize(text):
    return [t for t in re.findall(r"[A-Za-z0-9_]+", text.lower()) if len(t) > 3]


def find_excerpt(content_lines, keywords, window=2):
    if not content_lines:
        return []
    keyword_set = {k.lower() for k in keywords if k}
    for idx, line in enumerate(content_lines):
        lower = line.lower()
        if any(k in lower for k in keyword_set):
            start = max(0, idx - window)
            end = min(len(content_lines), idx + window + 1)
            return content_lines[start:end]
    return content_lines[: min(3, len(content_lines))]


def build_back(card_type, excerpt_lines, topic, anchors, h2_titles):
    lines = [line for line in excerpt_lines if line]
    if not lines:
        lines = [f"{topic} from the note context"]
    anchor = anchors[0] if anchors else topic
    if card_type == "MODEL":
        stages = lines[:2]
        if len(stages) < 2:
            stages = stages * 2
        return f"Steps: 1) {stages[0]} 2) {stages[1]} (via {anchor})"
    if card_type == "FAILURE_MODE":
        failure = lines[0]
        consequence = lines[1] if len(lines) > 1 else lines[0]
        return f"Consequence: {failure}. Then {anchor} produces {consequence}."
    if card_type == "COUNTER_EVIDENCE":
        counter = lines[0]
        condition = lines[1] if len(lines) > 1 else lines[0]
        return f"Counterexample: {counter}. Example: when {condition}, {anchor} does NOT apply."
    if card_type == "NEGATION":
        if len(anchors) >= 2:
            a, b = anchors[0], anchors[1]
        elif len(h2_titles) >= 2:
            a, b = h2_titles[0], h2_titles[1]
        else:
            a, b = anchor, "related concept"
        return (
            f"Mutation: {a} mutates state; {b} does not. "
            f"Return value: {a} returns a value; {b} returns a different value."
        )
    if card_type == "SYNTHESIS":
        if len(anchors) >= 2:
            a, b = anchors[0], anchors[1]
        elif len(h2_titles) >= 2:
            a, b = h2_titles[0], h2_titles[1]
        else:
            a, b = anchor, "related concept"
        return (
            f"Mutation: {a} mutates state; {b} does not. "
            f"Return value: {a} returns a value; {b} returns a different value."
        )
    return lines[0]


def classify_card(front, back):
    front_lower = front.lower()
    if "<pre" in back and "<code>" in back:
        return "CONSTRUCTIVE"
    if front_lower.startswith("what is "):
        return "DEFINITION"
    if front_lower.startswith("how do you") or front_lower.startswith("how to"):
        return "PROCEDURE"
    return "THEORY"


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError):
        return default


def pick_anchor_pool(meta, fallback):
    anchors = []
    if isinstance(meta, dict):
        anchor_meta = meta.get("anchors", {})
        if isinstance(anchor_meta, dict):
            anchors.extend(anchor_meta.get("methods", []))
            anchors.extend(anchor_meta.get("keywords", []))
    anchors = [a for a in anchors if a]
    if not anchors:
        anchors = [fallback]
    return anchors


def build_front(card_type, topic, anchors, h2_titles):
    anchor = anchors[0] if anchors else topic
    if card_type == "SYNTHESIS":
        if len(anchors) >= 2:
            a, b = anchors[0], anchors[1]
        elif len(h2_titles) >= 2:
            a, b = h2_titles[0], h2_titles[1]
        else:
            a, b = anchor, "related concept"
        return f"<strong>{topic}</strong><br>Compare {a} and {b} regarding mutation and return value."
    if card_type == "NEGATION":
        if len(anchors) >= 2:
            a, b = anchors[0], anchors[1]
        elif len(h2_titles) >= 2:
            a, b = h2_titles[0], h2_titles[1]
        else:
            a, b = anchor, "related concept"
        return f"<strong>{topic}</strong><br>How does {a} differ from {b}?"
    if card_type == "MODEL":
        return f"<strong>{topic}</strong><br>Explain/visualize how {anchor} works end-to-end."
    if card_type == "FAILURE_MODE":
        if anchor in {"const", "let", "var"}:
            misuse = f"reassign a {anchor} binding"
        elif anchor in {"push", "splice", "pop", "shift", "unshift", "sort", "reverse"}:
            misuse = f"mutate the array with {anchor} while iterating forward"
        else:
            misuse = f"call {anchor} with the wrong input type"
        return f"<strong>{topic}</strong><br>What goes wrong if you {misuse}?"
    if card_type == "COUNTER_EVIDENCE":
        return f"<strong>{topic}</strong><br>When does {anchor} NOT apply?"
    return (
        f"<strong>{topic}</strong><br>Explain/visualize how {anchor} works end-to-end."
    )


def main():
    parser = argparse.ArgumentParser(description="Append missing required card types.")
    parser.add_argument("--tsv", required=True, help="Path to TSV file.")
    parser.add_argument(
        "--doctrine", required=True, help="Path to doctrine_report.json."
    )
    parser.add_argument("--note-meta", required=True, help="Path to note_meta.json.")
    parser.add_argument("--note-path", required=True, help="Path to source note.")
    parser.add_argument("--vault", required=True, help="Vault name.")
    parser.add_argument("--vault-root", required=True, help="Vault root path.")
    parser.add_argument("--budget", required=False, help="Path to card_budget.json.")
    args = parser.parse_args()

    doctrine = load_json(args.doctrine, {})
    report = doctrine.get("doctrine_compliance_report", {})
    failures = set(report.get("failures", []))

    meta = load_json(args.note_meta, {})
    h2_titles = meta.get("h2_titles", [])
    topic = os.path.splitext(os.path.basename(args.note_path))[0]
    anchor_pool = pick_anchor_pool(meta, topic)

    target_constructive_max = None
    target_total_max = None
    if args.budget:
        budget = load_json(args.budget, {}).get("card_budget_plan", {})
        target_constructive_max = budget.get("target_constructive_max")
        target_total_max = budget.get("target_total_cards_max")

    rel = os.path.relpath(args.note_path, args.vault_root)
    url = encode_obsidian_url(args.vault, rel)

    missing_types = []
    if "missing_counter_evidence" in failures:
        missing_types.append("COUNTER_EVIDENCE")
    if "missing_failure_mode" in failures:
        missing_types.append("FAILURE_MODE")
    if "missing_model" in failures:
        missing_types.append("MODEL")
    if "missing_synthesis" in failures or "missing_cross_h2_synthesis" in failures:
        missing_types.append("SYNTHESIS")
    if "missing_negation" in failures:
        missing_types.append("NEGATION")

    if not missing_types:
        return 0

    try:
        with open(args.note_path, "r", encoding="utf-8") as handle:
            note_lines = handle.readlines()
    except OSError:
        note_lines = []
    content_lines = extract_content_lines(note_lines)

    with open(args.tsv, "r", encoding="utf-8") as handle:
        lines = handle.readlines()

    parsed = []
    for index, raw in enumerate(lines):
        parts = raw.rstrip("\n").split("\t")
        if len(parts) != 3:
            continue
        front, back, card_url = parts
        parsed.append(
            {
                "index": index,
                "front": front,
                "back": back,
                "url": card_url,
                "type": classify_card(front, back),
            }
        )

    card_by_index = {card["index"]: card for card in parsed}

    total_cards = len(parsed)
    additions = []
    replacements = {}

    candidate_indices = []
    for card in parsed:
        if card["type"] == "THEORY":
            candidate_indices.append(card["index"])
    for card in parsed:
        if card["type"] == "DEFINITION":
            candidate_indices.append(card["index"])
    for card in parsed:
        if card["type"] == "PROCEDURE":
            candidate_indices.append(card["index"])

    if target_constructive_max is not None:
        constructive = [card for card in parsed if card["type"] == "CONSTRUCTIVE"]
        if len(constructive) > int(target_constructive_max):
            extra = constructive[int(target_constructive_max) :]
            for card in extra:
                candidate_indices.append(card["index"])

    for missing in missing_types:
        if candidate_indices:
            target_index = candidate_indices.pop(0)
            original = card_by_index.get(target_index)
            if not original:
                continue
            keywords = (
                tokenize(original["front"])
                + tokenize(original["back"])
                + tokenize(topic)
            )
            excerpt = find_excerpt(content_lines, keywords)
            front = build_front(missing, topic, anchor_pool, h2_titles)
            back = build_back(missing, excerpt, topic, anchor_pool, h2_titles)
            front = sanitize_field(front)
            back = sanitize_field(back)
            replacements[target_index] = f"{front}\t{back}\t{original['url']}\n"
            continue

        max_total = (
            int(target_total_max) if target_total_max is not None else total_cards
        )
        if total_cards >= max_total:
            continue

        front = build_front(missing, topic, anchor_pool, h2_titles)
        excerpt = find_excerpt(content_lines, tokenize(front) + tokenize(topic))
        back = build_back(missing, excerpt, topic, anchor_pool, h2_titles)
        additions.append((sanitize_field(front), sanitize_field(back)))

    if replacements:
        for index, line in enumerate(lines):
            if index in replacements:
                lines[index] = replacements[index]
        with open(args.tsv, "w", encoding="utf-8") as handle:
            handle.writelines(lines)

    if additions:
        needs_newline = False
        try:
            with open(args.tsv, "rb") as handle:
                handle.seek(-1, os.SEEK_END)
                last_char = handle.read(1)
                needs_newline = last_char not in {b"\n", b""}
        except OSError:
            needs_newline = False
        with open(args.tsv, "a", encoding="utf-8") as handle:
            if needs_newline:
                handle.write("\n")
            for front, back in additions:
                handle.write(f"{front}\t{back}\t{url}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
