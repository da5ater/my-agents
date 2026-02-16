#!/usr/bin/env python3
import sys
import re
import argparse
import urllib.parse
from typing import List, Optional

# --- Manifesto Rules ---

BANNED_BACK_PHRASES = [
    "leads to incorrect behavior",
    "focuses on its own role",
    "not just a synonym",
    "end-to-end",
    "misused",
]

BANNED_FRONT_PATTERNS = [
    (
        re.compile(r"^explain ", re.IGNORECASE),
        "Generic 'Explain X' prompt. Use 'How does X work?' or 'Draw the diagram'.",
    ),
    (
        re.compile(r"^(is|are|does|can|should) ", re.IGNORECASE),
        "Yes/No question. Use 'When/How/Why' or 'What is the specific condition?'.",
    ),
    (
        re.compile(r"^(it|this|they) ", re.IGNORECASE),
        "Orphan pronoun. Explicitly name the concept.",
    ),
    (
        re.compile(r"^what goes wrong\?", re.IGNORECASE),
        "Vague failure mode. Specify the scenario.",
    ),
    (
        re.compile(r"^write the code example for", re.IGNORECASE),
        "Redundant phrasing. Use 'Implement [Function]'.",
    ),
]


def clean_field(text: str) -> str:
    """Normalize field content."""
    # Replace literal newlines with <br> just in case, though input should be single line
    text = text.replace("\\n", "<br>").replace("\n", "<br>").replace("\r", "")
    text = text.strip()
    return text


def validate_card(front: str, back: str) -> List[str]:
    """Check card content against Manifesto rules."""
    failures = []

    if not front:
        failures.append("Empty Front field")
    if not back:
        failures.append("Empty Back field")

    for phrase in BANNED_BACK_PHRASES:
        if phrase in back.lower():
            failures.append(f"Banned phrase in Back: '{phrase}'")

    for pattern, msg in BANNED_FRONT_PATTERNS:
        if pattern.search(front):
            failures.append(f"Front rule violation: {msg}")

    return failures


def process_line(line: str, vault: str, default_file: str) -> Optional[str]:
    """
    Parse, repair, and validate a TSV line.
    Returns the cleaned line (str) or None if invalid.
    """
    line = line.strip()
    if not line:
        return None

    parts = line.split("\t")

    front = ""
    back = ""
    url = ""

    # parse
    if len(parts) == 3:
        front, back, url = parts
    elif len(parts) == 2:
        # Ambiguous: Front/Back or Front/URL?
        # If 2nd part looks like URL, assume Front/URL (Back missing?)
        if "obsidian://" in parts[1]:
            front = parts[0]
            url = parts[1]
            back = "[MISSING BACK]"  # Mark as invalid implicitly?
        else:
            front, back = parts
    else:
        # >3 or <2
        # If >3, maybe tabs in content?
        # Try to salvage: First is Front, Last is URL, middle is Back
        if len(parts) > 3:
            front = parts[0]
            if "obsidian://" in parts[-1]:
                url = parts[-1]
                back = "    ".join(parts[1:-1])
            else:
                # No URL at end, maybe just Front/Back with tabs?
                back = "    ".join(parts[1:])
        else:
            return None

    # clean
    front = clean_field(front)
    back = clean_field(back)
    url = url.strip()

    # infer url
    if not url or "obsidian://" not in url:
        if default_file:
            # Construct URL
            # default_file should be relative path from vault root?
            # or absolute? We assume relative or filename.
            # standard format: obsidian://open?vault=NAME&file=PATH
            clean_path = default_file
            if clean_path.endswith(".md"):
                clean_path = clean_path[:-3]
            encoded_path = urllib.parse.quote(clean_path)
            url = f"obsidian://open?vault={vault}&file={encoded_path}"
        else:
            # Fatal: No URL and can't infer
            # sys.stderr.write(f"Skipping line: No URL found and no default file provided. Content: {front[:20]}...\n")
            return None

    # validate
    errors = validate_card(front, back)
    if errors:
        for err in errors:
            sys.stderr.write(f"[Validation Failed] {err} | Card: {front[:40]}...\n")
        return None

    return f"{front}\t{back}\t{url}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default="mohamed")
    parser.add_argument(
        "--default-file", help="Path to current file (for URL inference)"
    )
    args = parser.parse_args()

    for line in sys.stdin:
        result = process_line(line, args.vault, args.default_file or "")
        if result:
            print(result)


if __name__ == "__main__":
    main()
