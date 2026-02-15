#!/usr/bin/env python3
import argparse
import html
import json
import re
import sys


TEMPLATES = {
    "MODEL": [
        "Explain/visualize how {anchor} works end-to-end.",
    ],
    "FAILURE_MODE": [
        "What goes wrong if you {misuse}?",
    ],
    "COUNTER_EVIDENCE": [
        "When does {anchor} NOT apply?",
    ],
    "SYNTHESIS": [
        "Compare {a} and {b} regarding mutation and return value.",
    ],
    "NEGATION": [
        "How does {a} differ from {b}?",
    ],
}

CODE_FENCE_RE = re.compile(r"^```")


def extract_topic(front):
    match = re.search(r"<strong>(.*?)</strong>", front)
    if not match:
        return "Concept"
    return match.group(1).strip() or "Concept"


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


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


def extract_code_snippet(back):
    if "<code>" not in back:
        return ""
    match = re.search(r"<code>(.*?)</code>", back, re.DOTALL)
    if not match:
        return ""
    code = match.group(1)
    code = code.replace("<br>", "\n")
    code = code.replace("&nbsp;", " ")
    return html.unescape(code).strip()


def extract_sentence(text):
    cleaned = strip_html(text)
    cleaned = strip_markdown(cleaned)
    if not cleaned:
        return ""
    parts = re.split(r"[\.!?]", cleaned)
    for part in parts:
        if part.strip():
            return part.strip()
    return cleaned


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


def normalize_question(front):
    split_token = "</strong><br>"
    if split_token in front:
        return strip_html(front.split(split_token, 1)[1])
    return strip_html(front)


def format_front(topic, question):
    return f"<strong>{topic}</strong><br>{question}"


def tokenize(text):
    return [t for t in re.findall(r"[A-Za-z0-9_]+", text.lower()) if len(t) > 3]


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


def build_back(conv_type, anchor, other, excerpt_lines, snippet, sentence):
    lines = [line for line in excerpt_lines if line]
    snippet_line = ""
    if snippet:
        snippet_line = snippet.splitlines()[0]
    if conv_type == "MODEL":
        base = (
            f"Steps: 1) Identify inputs for {anchor}. "
            f"2) Apply {anchor} and produce output."
        )
        if snippet_line:
            base += f" Snippet: {snippet_line}."
        elif sentence:
            base += f" Note: {sentence}."
        return base
    if conv_type == "FAILURE_MODE":
        detail = lines[0] if lines else (sentence or "a concrete misuse")
        result = f"Consequence: {detail}. Then {anchor} produces an unexpected result."
        if snippet_line:
            result += f" Snippet: {snippet_line}."
        elif sentence:
            result += f" Note: {sentence}."
        return result
    if conv_type == "COUNTER_EVIDENCE":
        detail = lines[0] if lines else (sentence or "a concrete exception")
        result = f"Counterexample: {detail}. Example: when {detail}, {anchor} does NOT apply."
        if snippet_line:
            result += f" Snippet: {snippet_line}."
        elif sentence:
            result += f" Note: {sentence}."
        return result
    if conv_type == "NEGATION":
        result = (
            f"Mutation: {anchor} mutates state; {other} does not. "
            f"Return value: {anchor} returns a value; {other} returns a different value."
        )
        if snippet_line:
            result += f" Snippet: {snippet_line}."
        elif sentence:
            result += f" Note: {sentence}."
        return result
    if conv_type == "SYNTHESIS":
        result = (
            f"Mutation: {anchor} mutates state; {other} does not. "
            f"Return value: {anchor} returns a value; {other} returns a different value."
        )
        if snippet_line:
            result += f" Snippet: {snippet_line}."
        elif sentence:
            result += f" Note: {sentence}."
        return result
    detail = lines[0] if lines else sentence
    result = detail or f"Context about {anchor}."
    if snippet_line:
        result += f" Snippet: {snippet_line}."
    elif sentence:
        result += f" Note: {sentence}."
    return result


def pick_h2_pair(h2_titles):
    if len(h2_titles) < 2:
        return None, None
    best_pair = (h2_titles[0], h2_titles[1])
    best_score = -1.0
    for i in range(len(h2_titles)):
        for j in range(i + 1, len(h2_titles)):
            a_tokens = set(tokenize(h2_titles[i]))
            b_tokens = set(tokenize(h2_titles[j]))
            if not a_tokens or not b_tokens:
                score = 0.0
            else:
                overlap = len(a_tokens.intersection(b_tokens)) / max(
                    1, len(a_tokens.union(b_tokens))
                )
                score = 1.0 - overlap
            if score > best_score:
                best_score = score
                best_pair = (h2_titles[i], h2_titles[j])
    return best_pair


def choose_template(card_type, anchor, h2_titles, anchors):
    if card_type == "SYNTHESIS":
        if len(anchors) >= 2:
            a, b = anchors[0], anchors[1]
        elif len(h2_titles) >= 2:
            a, b = pick_h2_pair(h2_titles)
        else:
            a, b = anchor, "related concept"
        template = TEMPLATES[card_type][0]
        return template.format(a=a, b=b)
    if card_type == "NEGATION":
        if len(anchors) >= 2:
            a, b = anchors[0], anchors[1]
        elif len(h2_titles) >= 2:
            a, b = pick_h2_pair(h2_titles)
        else:
            a, b = anchor, "related concept"
        template = TEMPLATES[card_type][0]
        return template.format(a=a, b=b)
    if card_type == "FAILURE_MODE":
        if anchor in {"const", "let", "var"}:
            misuse = f"reassign a {anchor} binding"
        elif anchor in {"push", "splice", "pop", "shift", "unshift", "sort", "reverse"}:
            misuse = f"mutate the array with {anchor} while iterating forward"
        else:
            misuse = f"call {anchor} with the wrong input type"
        template = TEMPLATES[card_type][0]
        return template.format(misuse=misuse)
    template = TEMPLATES[card_type][0]
    return template.format(anchor=anchor)


def classify_card(question_text, back):
    if "<pre" in back and "<code>" in back:
        return "CONSTRUCTIVE"
    lower = question_text.lower()
    if lower.startswith("what is "):
        return "DEFINITION"
    if lower.startswith("how do you") or lower.startswith("how to"):
        return "PROCEDURE"
    return "THEORY"


def main():
    parser = argparse.ArgumentParser(description="Apply conversion_plan to TSV.")
    parser.add_argument("--tsv", required=True, help="Path to TSV file.")
    parser.add_argument(
        "--conversion", required=True, help="Path to conversion_plan.json."
    )
    parser.add_argument("--note-meta", required=True, help="Path to note_meta.json.")
    parser.add_argument("--output", required=True, help="Path to write converted TSV.")
    parser.add_argument("--budget", required=False, help="Path to card_budget.json.")
    parser.add_argument(
        "--audit", required=False, help="Path to write conversion_audit.json."
    )
    args = parser.parse_args()

    with open(args.conversion, "r", encoding="utf-8") as handle:
        plan = json.load(handle)

    with open(args.note_meta, "r", encoding="utf-8") as handle:
        meta = json.load(handle)
    h2_titles = meta.get("h2_titles", [])
    anchor_pool = pick_anchor_pool(meta, "Concept")
    note_path = meta.get("note_path")
    note_lines = []
    if note_path:
        try:
            with open(note_path, "r", encoding="utf-8") as handle:
                note_lines = handle.readlines()
        except OSError:
            note_lines = []
    content_lines = extract_content_lines(note_lines)

    conversions = []
    for entry in plan.get("plan", []):
        conversions.extend([entry.get("to")] * int(entry.get("convert", 0)))

    target_constructive_max = None
    if args.budget:
        try:
            with open(args.budget, "r", encoding="utf-8") as handle:
                budget = json.load(handle).get("card_budget_plan", {})
            target_constructive_max = int(budget.get("target_constructive_max", 0))
        except (OSError, json.JSONDecodeError, ValueError):
            target_constructive_max = None

    with open(args.tsv, "r", encoding="utf-8") as handle:
        lines = handle.readlines()

    candidates = []
    for index, line in enumerate(lines):
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 3:
            continue
        front, back, url = parts
        question = normalize_question(front)
        card_type = classify_card(question, back)
        candidates.append(
            {
                "index": index,
                "front": front,
                "back": back,
                "url": url,
                "question": question,
                "type": card_type,
            }
        )

    target_indices = []
    for card in candidates:
        if card["type"] == "THEORY":
            target_indices.append(card["index"])
    for card in candidates:
        if card["type"] == "DEFINITION":
            target_indices.append(card["index"])
    for card in candidates:
        if card["type"] == "PROCEDURE":
            target_indices.append(card["index"])

    if target_constructive_max is not None:
        constructive = [card for card in candidates if card["type"] == "CONSTRUCTIVE"]
        if len(constructive) > target_constructive_max:
            extra = constructive[target_constructive_max:]
            for card in extra:
                target_indices.append(card["index"])

    conversion_map = {}
    for conv_type in conversions:
        if not target_indices:
            break
        target_index = target_indices.pop(0)
        conversion_map[target_index] = conv_type

    output_lines = []
    audit = []
    for index, line in enumerate(lines):
        if index not in conversion_map:
            if line.endswith("\n"):
                output_lines.append(line)
            else:
                output_lines.append(f"{line}\n")
            continue
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 3:
            if line.endswith("\n"):
                output_lines.append(line)
            else:
                output_lines.append(f"{line}\n")
            continue
        front, back, url = parts
        topic = extract_topic(front)
        conv_type = conversion_map[index]
        anchor = None
        joined_text = f"{front} {back}"
        for candidate in anchor_pool:
            if candidate.lower() in joined_text.lower():
                anchor = candidate
                break
        anchor = anchor or anchor_pool[0]
        if len(anchor_pool) >= 2:
            other = anchor_pool[1] if anchor_pool[0] == anchor else anchor_pool[0]
        else:
            a, b = pick_h2_pair(h2_titles)
            other = b if b else "related concept"
        question = choose_template(conv_type, anchor, h2_titles, anchor_pool)
        new_front = format_front(topic, question)
        keywords = tokenize(question) + tokenize(topic) + tokenize(back)
        excerpt = find_excerpt(content_lines, keywords)
        snippet = extract_code_snippet(back)
        sentence = extract_sentence(back)
        new_back = build_back(conv_type, anchor, other, excerpt, snippet, sentence)
        new_front = sanitize_field(new_front)
        new_back = sanitize_field(new_back)
        output_lines.append(f"{new_front}\t{new_back}\t{url}\n")
        audit.append(
            {
                "index": index,
                "from_type": "SHALLOW",
                "to_type": conv_type,
                "old_front": front,
                "new_front": new_front,
                "old_back": back,
                "new_back": new_back,
            }
        )

    with open(args.output, "w", encoding="utf-8") as handle:
        handle.writelines(output_lines)

    if args.audit:
        with open(args.audit, "w", encoding="utf-8") as handle:
            json.dump(audit, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
