#!/usr/bin/env python3
import sys
import re
import argparse
import urllib.parse
from typing import List, Optional, Tuple

# --- Configuration & Constants ---

CONFIG = {
    "BANNED_BACK_PHRASES": [
        "leads to incorrect behavior",
        "focuses on its own role",
        "not just a synonym",
        "end-to-end",
        "misused",
        "allows for",
        "provides a way to",
    ],
    "BANNED_FRONT_PATTERNS": [
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
    ],
}

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

    for phrase in CONFIG["BANNED_BACK_PHRASES"]:
        if phrase in back.lower():
            failures.append(f"Banned phrase in Back: '{phrase}'")

    for pattern, msg in CONFIG["BANNED_FRONT_PATTERNS"]:
        if pattern.search(front):
            failures.append(f"Front rule violation: {msg}")

    return failures

def process_line(line: str, line_num: int, vault: str, default_file: str) -> Tuple[Optional[str], List[str]]:
    """
    Parse, repair, and validate a TSV line.
    Returns (cleaned_line, errors).
    """
    line = line.strip()
    if not line:
        return None, []

    parts = line.split("\t")
    front = ""
    back = ""
    url = ""

    # Parse columns with heuristic recovery
    if len(parts) == 3:
        front, back, url = parts
    elif len(parts) == 2:
        if "obsidian://" in parts[1]:
            front = parts[0]
            url = parts[1]
            back = "[MISSING BACK]" 
        else:
            front, back = parts
    else:
        # Try to salvage broken tabs
        if len(parts) > 3:
            front = parts[0]
            if "obsidian://" in parts[-1]:
                url = parts[-1]
                back = "    ".join(parts[1:-1])
            else:
                back = "    ".join(parts[1:])
        else:
            return None, [f"Invalid column count: {len(parts)} (Required: 3)"]

    # Clean content
    front = clean_field(front)
    back = clean_field(back)
    url = url.strip()

    # URL Inference
    if not url or "obsidian://" not in url:
        if default_file:
            clean_path = default_file
            if clean_path.endswith(".md"):
                clean_path = clean_path[:-3]
            encoded_path = urllib.parse.quote(clean_path)
            url = f"obsidian://open?vault={vault}&file={encoded_path}"
        else:
            return None, ["Missing URL and no default file provided to infer it."]

    # Validation
    errors = validate_card(front, back)
    if errors:
        return None, errors

    return f"{front}\t{back}\t{url}", []

def main():
    parser = argparse.ArgumentParser(description="Validate Ankify TSV output against Manifesto rules.")
    parser.add_argument("--vault", default="mohamed", help="Obsidian vault name for URL generation.")
    parser.add_argument("--default-file", help="Path to current note for URL inference.")
    parser.add_argument("input_file", nargs="?", type=argparse.FileType("r"), default=sys.stdin, help="Input TSV file (default: stdin)")
    
    args = parser.parse_args()

    line_count = 0
    error_count = 0

    for line in args.input_file:
        line_count += 1
        clean_line, errors = process_line(line, line_count, args.vault, args.default_file or "")
        
        if errors:
            error_count += 1
            for err in errors:
                # Structured error output for Agent to parse
                sys.stderr.write(f"Line {line_count}: [Error] {err} | Content: {line[:50].strip()}...\n")
        elif clean_line:
            sys.stdout.write(clean_line + "\n")

    if error_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
