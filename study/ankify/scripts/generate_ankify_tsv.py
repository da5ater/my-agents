#!/usr/bin/env python3
import argparse
import html
import os
import re
import keyword
from pathlib import Path


H2_RE = re.compile(r"^##\s+(.*)$")
H3_RE = re.compile(r"^###\s+(.*)$")
BLOCKQUOTE_RE = re.compile(r"^>\s?(.*)$")
CODE_FENCE_RE = re.compile(r"^```")
LINE_COMMENT_RE = re.compile(r"^\s*(//|#)\s?(.*)$")
INLINE_COMMENT_RE = re.compile(r"//(.*)$")
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
IDENT_RE = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
METHOD_CALL_RE = re.compile(r"\.([A-Za-z_$][A-Za-z0-9_$]*)\s*\(")
TERM_RE = re.compile(
    r"^([A-Za-z0-9_\-\s]{2,80})\s+(is|are|refers to|means)\b", re.IGNORECASE
)
IMPORT_RE = re.compile(r"^\s*import\s+.*")
REQUIRE_RE = re.compile(r"require\s*\(")

GENERIC_H3 = {
    "notes",
    "definitions",
    "configuration",
    "technical procedures",
    "code implementation",
    "distinctions & negations",
    "counter-evidence",
}

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
    "console",
    "log",
}

ANCHOR_KEYWORDS = {
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
}


def slug_title(title):
    return title.strip()


def encode_obsidian_url(vault, path):
    rel = path.replace(".md", "")
    rel = rel.replace("/", "%2F").replace(" ", "%20")
    return f"obsidian://open?vault={vault}&file={rel}"


def serialize_code(code):
    code = code.rstrip("\n")
    code = html.escape(code)
    code = code.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    code = code.replace(" ", "&nbsp;")
    code = code.replace("\n", "<br>")
    return (
        "<pre style='text-align:left; font-family:monospace;'><code>"
        + code
        + "</code></pre>"
    )


def sanitize_field(text):
    text = text.replace("\t", " ")
    text = text.replace("\n", "<br>")
    return text


def add_unique(items, value):
    if value in items:
        return
    items.append(value)


def extract_anchor_tokens(code_blocks):
    methods = []
    keywords = []
    for block in code_blocks:
        code = block.get("code") or ""
        for method in METHOD_CALL_RE.findall(code):
            add_unique(methods, method)
        lower = code.lower()
        for keyword_token in ANCHOR_KEYWORDS:
            if re.search(r"\b" + re.escape(keyword_token) + r"\b", lower):
                add_unique(keywords, keyword_token)
    anchors = []
    for item in methods + keywords:
        if item and item not in anchors:
            anchors.append(item)
    return anchors


def parse_note(text):
    h2_titles = []
    h3_titles = []
    blocks = []
    code_blocks = []
    current_h2 = None
    current_h3 = None
    current_blockquote = []
    in_code = False
    code_lines = []

    for line in text.splitlines():
        if CODE_FENCE_RE.match(line):
            if in_code:
                code_blocks.append(
                    {
                        "h2": current_h2,
                        "h3": current_h3,
                        "code": "\n".join(code_lines),
                    }
                )
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        h2 = H2_RE.match(line)
        h3 = H3_RE.match(line)
        if h2:
            if current_blockquote:
                blocks.append(
                    {
                        "h2": current_h2,
                        "h3": current_h3,
                        "quote": " ".join(current_blockquote).strip(),
                    }
                )
                current_blockquote = []
            current_h2 = slug_title(h2.group(1))
            current_h3 = None
            h2_titles.append(current_h2)
            continue
        if h3:
            if current_blockquote:
                blocks.append(
                    {
                        "h2": current_h2,
                        "h3": current_h3,
                        "quote": " ".join(current_blockquote).strip(),
                    }
                )
                current_blockquote = []
            current_h3 = slug_title(h3.group(1))
            h3_titles.append(current_h3)
            continue

        block = BLOCKQUOTE_RE.match(line)
        if block:
            current_blockquote.append(block.group(1))
        elif current_blockquote:
            blocks.append(
                {
                    "h2": current_h2,
                    "h3": current_h3,
                    "quote": " ".join(current_blockquote).strip(),
                }
            )
            current_blockquote = []

    if current_blockquote:
        blocks.append(
            {
                "h2": current_h2,
                "h3": current_h3,
                "quote": " ".join(current_blockquote).strip(),
            }
        )

    return h2_titles, h3_titles, blocks, code_blocks


def normalize_text(text):
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^A-Za-z0-9_]+", " ", text)
    return [token for token in text.lower().split() if token]


def overlap_ratio(tokens_a, tokens_b):
    if not tokens_a or not tokens_b:
        return 0.0
    counts_a = {}
    counts_b = {}
    for token in tokens_a:
        counts_a[token] = counts_a.get(token, 0) + 1
    for token in tokens_b:
        counts_b[token] = counts_b.get(token, 0) + 1
    common = 0
    for token, count in counts_a.items():
        common += min(count, counts_b.get(token, 0))
    return common / max(1, len(tokens_a))


def extract_comments(code):
    comments = []
    code = BLOCK_COMMENT_RE.sub(" ", code)
    for line in code.splitlines():
        match = LINE_COMMENT_RE.match(line)
        if match:
            comment = match.group(2).strip()
            if comment:
                comments.append(comment)
        else:
            inline = INLINE_COMMENT_RE.search(line)
            if inline:
                comment = inline.group(1).strip()
                if comment:
                    comments.append(comment)
    return comments


def extract_imports(code):
    imports = []
    for line in code.splitlines():
        if IMPORT_RE.match(line):
            imports.append(line.strip())
        elif REQUIRE_RE.search(line):
            imports.append(line.strip())
    return imports


def extract_identifiers(code):
    tokens = []
    seen = set()
    for token in IDENT_RE.findall(code):
        lower = token.lower()
        if lower in STOPWORDS:
            continue
        if keyword.iskeyword(token):
            continue
        if token in seen:
            continue
        seen.add(token)
        tokens.append(token)
    return tokens[:6]


def infer_term_from_quote(quote):
    match = TERM_RE.match(quote.strip())
    if match:
        return match.group(1).strip()
    return ""


def clean_quote(quote):
    quote = re.sub(r"\[!.*?\]", "", quote)
    return quote.strip()


def chunk_code(code, max_lines=2):
    lines = [line.rstrip() for line in code.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    if len(lines) <= max_lines:
        return ["\n".join(lines)]

    return ["\n".join(lines[:max_lines])]


def build_cards(topic, h2_titles, blocks, code_blocks, full_text):
    cards = []
    seen_terms = set()
    target_definition_max = 1
    target_constructive_max = min(2, len(code_blocks))

    anchors = extract_anchor_tokens(code_blocks)
    anchor_pool = list(anchors)
    if not anchor_pool:
        anchor_pool = [title for title in h2_titles if title] or [topic]

    is_high_complexity = bool(
        len(anchors) >= 8 or len(h2_titles) >= 3 or len(code_blocks) > 1
    )
    max_total = 8 if is_high_complexity else 6
    deep_limit = 3

    def pick_anchor(default_value):
        if anchor_pool:
            return anchor_pool[0]
        return default_value

    def pick_anchor_pair():
        if len(anchor_pool) >= 2:
            return anchor_pool[0], anchor_pool[1]
        if len(h2_titles) >= 2:
            return h2_titles[0], h2_titles[1]
        return topic, "related concept"

    def pick_code_line(code):
        for line in code.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if stripped in {"{", "}", "};", "}", "},", ")", ");", "]", "],"}:
                continue
            if LINE_COMMENT_RE.match(line):
                continue
            return line
        return ""

    definition_cards = []
    for block in blocks:
        if len(definition_cards) >= target_definition_max:
            break
        quote = block.get("quote")
        if not quote:
            continue
        quote = clean_quote(quote)
        term = infer_term_from_quote(quote)
        if not term:
            term = block.get("h2") or block.get("h3") or topic
        if not term or term.lower() in seen_terms:
            continue
        seen_terms.add(term.lower())
        definition_cards.append(
            (
                sanitize_field(f"<strong>{topic}</strong><br>Define {term}."),
                sanitize_field(quote),
            )
        )

    deep_cards = []
    anchor = pick_anchor(topic)
    model_front = (
        f"<strong>{topic}</strong><br>Explain/visualize how {anchor} works end-to-end."
    )
    model_back = (
        f"Steps: 1) Identify inputs for {anchor}. 2) Apply {anchor} and produce output."
    )
    deep_cards.append((sanitize_field(model_front), sanitize_field(model_back)))

    failure_anchor = pick_anchor(topic)
    if failure_anchor in {"const", "let", "var"}:
        misuse = f"reassign a {failure_anchor} binding"
        consequence = f"Then {failure_anchor} throws and the assignment fails."
    elif failure_anchor in {
        "push",
        "splice",
        "pop",
        "shift",
        "unshift",
        "sort",
        "reverse",
    }:
        misuse = f"mutate the array with {failure_anchor} while iterating forward"
        consequence = "Then the iteration skips or repeats elements."
    else:
        misuse = f"call {failure_anchor} with the wrong input type"
        consequence = f"Then {failure_anchor} returns an unexpected value and downstream logic breaks."
    failure_front = f"<strong>{topic}</strong><br>What goes wrong if you {misuse}?"
    failure_back = f"Consequence: {consequence}"
    deep_cards.append((sanitize_field(failure_front), sanitize_field(failure_back)))

    counter_anchor = pick_anchor(topic)
    counter_context = "the input is empty"
    for line in full_text.splitlines():
        lower = line.lower()
        if any(
            word in lower for word in ["unless", "except", "not apply", "exception"]
        ):
            counter_context = clean_quote(line)
            break
    counter_front = f"<strong>{topic}</strong><br>When does {counter_anchor} NOT apply?"
    counter_back = (
        f"Counterexample: when {counter_context}, {counter_anchor} does NOT apply. "
        f"Example: {counter_context}."
    )
    deep_cards.append((sanitize_field(counter_front), sanitize_field(counter_back)))

    neg_a, neg_b = pick_anchor_pair()
    neg_front = f"<strong>{topic}</strong><br>How does {neg_a} differ from {neg_b}?"
    neg_back = (
        f"Mutation: {neg_a} mutates state; {neg_b} does not. "
        f"Return value: {neg_a} returns a new value; {neg_b} returns a different result."
    )
    deep_cards.append((sanitize_field(neg_front), sanitize_field(neg_back)))

    syn_a, syn_b = pick_anchor_pair()
    syn_front = f"<strong>{topic}</strong><br>Compare {syn_a} and {syn_b} regarding mutation and return value."
    syn_back = (
        f"Mutation: {syn_a} mutates state; {syn_b} does not. "
        f"Return value: {syn_a} returns a value; {syn_b} returns a different value."
    )
    deep_cards.append((sanitize_field(syn_front), sanitize_field(syn_back)))

    deep_cards = deep_cards[:deep_limit]

    scored_blocks = []
    for block in code_blocks:
        heading = block.get("h3") or block.get("h2") or topic
        if heading and heading.lower() in GENERIC_H3:
            heading = block.get("h2") or topic
        code = (block.get("code") or "").strip()
        if not code:
            continue

        identifiers = extract_identifiers(code)
        score = len(code.splitlines()) + (len(identifiers) * 2)
        if block.get("h2"):
            score += 2
        if block.get("h3"):
            score += 1
        scored_blocks.append(
            {
                "heading": heading,
                "code": code,
                "score": score,
                "identifiers": identifiers,
            }
        )

    scored_blocks.sort(key=lambda item: item["score"], reverse=True)
    selected_blocks = scored_blocks[:target_constructive_max]

    constructive_cards = []
    for block in selected_blocks:
        code = block.get("code") or ""
        identifiers = block.get("identifiers") or []

        imports = extract_imports(code)
        comments = extract_comments(code)

        context_parts = []
        if imports:
            context_parts.append("Imports: " + ", ".join(imports[:2]))
        if identifiers:
            context_parts.append("Variables: " + ", ".join(identifiers[:5]))
        if comments:
            context_parts.append("Context: " + "; ".join(comments[:2]))
        if not context_parts:
            context_parts.append("Context: use the identifiers shown in the snippet")

        line = pick_code_line(code)
        if not line:
            continue
        line = line.rstrip()

        method_match = METHOD_CALL_RE.search(line)
        method = method_match.group(1) if method_match else ""
        obj_match = None
        if method:
            obj_match = re.search(
                r"([A-Za-z_$][A-Za-z0-9_$]*)\s*\.\s*" + re.escape(method), line
            )
        obj = (
            obj_match.group(1)
            if obj_match
            else (identifiers[0] if identifiers else "value")
        )
        assign_match = re.match(r"\s*([A-Za-z_$][A-Za-z0-9_$]*)\s*=", line)
        assign_target = assign_match.group(1) if assign_match else ""

        if method:
            task = f"Write the line that calls {method} on {obj}."
        elif assign_target:
            task = f"Write the line that assigns {assign_target}."
        else:
            continue

        prompt = (
            f"<strong>{topic}</strong><br>"
            f"Given: {'; '.join(context_parts)}<br>"
            f"Task: {task}"
        )
        constructive_cards.append((sanitize_field(prompt), serialize_code(line)))

    cards.extend(constructive_cards)
    cards.extend(deep_cards)
    cards.extend(definition_cards)

    if len(cards) > max_total:
        trimmed = []
        dropped = 0
        for front, back in cards:
            if len(trimmed) >= max_total:
                dropped += 1
                continue
            trimmed.append((front, back))
        cards = trimmed

    return cards


def dedupe_cards(cards):
    kept = []
    front_tokens = []
    back_tokens = []
    code_backs = set()
    for front, back in cards:
        ft = normalize_text(front)
        bt = normalize_text(back)

        front_overlap = 0.0
        back_overlap = 0.0
        for prior_ft in front_tokens:
            front_overlap = max(front_overlap, overlap_ratio(ft, prior_ft))
        for prior_bt in back_tokens:
            back_overlap = max(back_overlap, overlap_ratio(bt, prior_bt))
        if front_overlap > 0.85 and back_overlap > 0.85:
            continue

        if "<pre" in back and "<code>" in back:
            if back in code_backs:
                continue
            code_backs.add(back)

        kept.append((front, back))
        front_tokens.append(ft)
        back_tokens.append(bt)

    return kept


def validate_output_lines(lines):
    issues = {
        "bad_cols": 0,
        "placeholder_context": 0,
        "code_line_over": 0,
        "duplicate_fronts": 0,
        "duplicate_backs": 0,
        "duplicate_code_backs": 0,
    }
    front_tokens = {}
    back_tokens = {}
    code_backs = {}

    for line in lines:
        parts = line.split("\t")
        if len(parts) != 3:
            issues["bad_cols"] += 1
            continue
        front, back, url = parts

        if "Given: [Inputs/Context]" in front:
            issues["placeholder_context"] += 1

        if "<pre" in back and "<code>" in back:
            if back.count("<br>") + 1 > 2:
                issues["code_line_over"] += 1
            if back in code_backs.get(url, set()):
                issues["duplicate_code_backs"] += 1
            code_backs.setdefault(url, set()).add(back)

        ft = normalize_text(front)
        bt = normalize_text(back)
        max_front = 0.0
        max_back = 0.0
        for prior in front_tokens.get(url, []):
            max_front = max(max_front, overlap_ratio(ft, prior))
        for prior in back_tokens.get(url, []):
            max_back = max(max_back, overlap_ratio(bt, prior))
        if max_front > 0.85 and max_back > 0.85:
            issues["duplicate_fronts"] += 1
            issues["duplicate_backs"] += 1
        front_tokens.setdefault(url, []).append(ft)
        back_tokens.setdefault(url, []).append(bt)

    return issues


def repair_output_lines(lines):
    repaired = []
    front_tokens = {}
    back_tokens = {}
    code_backs = {}

    for line in lines:
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        front, back, url = parts

        if "Given: [Inputs/Context]" in front:
            front = front.replace(
                "Given: [Inputs/Context]",
                "Given: use the identifiers shown in the snippet",
            )

        ft = normalize_text(front)
        bt = normalize_text(back)
        max_front = 0.0
        max_back = 0.0
        for prior in front_tokens.get(url, []):
            max_front = max(max_front, overlap_ratio(ft, prior))
        for prior in back_tokens.get(url, []):
            max_back = max(max_back, overlap_ratio(bt, prior))
        if max_front > 0.85 and max_back > 0.85:
            continue

        if "<pre" in back and "<code>" in back:
            if back in code_backs.get(url, set()):
                continue
            code_backs.setdefault(url, set()).add(back)

        repaired.append(f"{front}\t{back}\t{url}")
        front_tokens.setdefault(url, []).append(ft)
        back_tokens.setdefault(url, []).append(bt)

    return repaired


def main():
    parser = argparse.ArgumentParser(description="Generate ankify TSV from notes.")
    parser.add_argument("--input", required=True, help="Path to folder with notes.")
    parser.add_argument("--output", required=True, help="Path to output TSV.")
    parser.add_argument("--vault", required=True, help="Vault name for obsidian URLs.")
    args = parser.parse_args()

    input_path = Path(args.input)
    max_iter = int(os.environ.get("MAX_ITER", "3"))
    output_lines = []

    for path in sorted(input_path.rglob("*.md")):
        if any(part in {".git", ".obsidian", "node_modules"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        topic = path.stem
        h2_titles, h3_titles, blocks, code_blocks = parse_note(text)
        cards = build_cards(topic, h2_titles, blocks, code_blocks, text)
        cards = dedupe_cards(cards)

        rel = str(path.relative_to(Path("/mnt/data/obsidian/mohamed")))
        url = encode_obsidian_url(args.vault, rel)
        for front, back in cards:
            output_lines.append(
                f"{sanitize_field(front)}\t{sanitize_field(back)}\t{url}"
            )

    for _ in range(max_iter):
        issues = validate_output_lines(output_lines)
        if all(value == 0 for value in issues.values()):
            break
        repaired = repair_output_lines(output_lines)
        if repaired == output_lines:
            break
        output_lines = repaired

    output_text = "\n".join(output_lines)
    if output_text and not output_text.endswith("\n"):
        output_text += "\n"
    Path(args.output).write_text(output_text, encoding="utf-8")


if __name__ == "__main__":
    main()
