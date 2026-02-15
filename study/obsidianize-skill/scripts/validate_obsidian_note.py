#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def find_frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, min(len(lines), 200)):
        if lines[i].strip() == "---":
            return (0, i)
    return None


def has_path_citation(line: str) -> bool:
    if re.search(r"\b(Path|File path|File):", line):
        return True
    backticks = re.findall(r"`([^`]+)`", line)
    for token in backticks:
        if "/" in token or "\\" in token:
            return True
    return False


def validate(text: str):
    errors = []
    lines = text.splitlines()

    fm = find_frontmatter(lines)
    if fm is None:
        errors.append("Missing or invalid YAML frontmatter (--- ... --- at top)")
        start_body = 0
    else:
        start_body = fm[1] + 1

    in_code = False
    code_start_line = None
    last_nonempty = ""
    h2_count = 0
    body_lines = 0
    summary_found = False
    artifact_markers = {
        "summary_artifacts",
        "stage2_analysis_artifacts",
        "internalization_report",
        "card_budget_plan",
        "doctrine_compliance_report",
    }

    first_content_checked = False
    for i, raw in enumerate(lines[start_body:], start=start_body):
        line = raw.rstrip("\n")

        if line.strip() == "":
            continue

        if not first_content_checked:
            first_content_checked = True
            if not line.startswith("## "):
                errors.append(
                    "File must start with an H2 Atomic Section after frontmatter"
                )

        if not in_code:
            body_lines += 1

        if line.startswith("```"):
            if not in_code:
                lang = line.strip()[3:]
                if lang == "":
                    errors.append(
                        f"Code block missing language specifier at line {i + 1}"
                    )
                if not has_path_citation(last_nonempty):
                    errors.append(
                        f"Missing file path citation before code block at line {i + 1}"
                    )
                in_code = True
                code_start_line = i + 1
            else:
                in_code = False
                code_start_line = None
            last_nonempty = line
            continue

        if in_code:
            continue

        if line.startswith("# "):
            errors.append(f"H1 header found at line {i + 1}")

        if line.startswith("## "):
            if line.strip() == "## Pre-Generation Summary":
                summary_found = True
            else:
                h2_count += 1
        elif line.startswith("### "):
            pass
        elif re.match(r"^#{4,}\s+", line):
            errors.append(f"Heading deeper than H3 found at line {i + 1}")

        if line.strip() == "| Section | Summary |":
            summary_found = True
        if any(marker in line for marker in artifact_markers):
            summary_found = True

        last_nonempty = line

    if in_code:
        errors.append(f"Unclosed code block starting at line {code_start_line}")

    if summary_found:
        errors.append(
            "Process artifacts found in file (summary table or Pre-Generation Summary)"
        )

    if body_lines > 0:
        density = h2_count / max(body_lines, 1)
        if density > 0.2:
            errors.append("H2 density ratio exceeds 0.2")

    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: validate_obsidian_note.py <path|->")
        return 2
    if sys.argv[1] == "-":
        text = sys.stdin.read()
        if not text:
            print("Empty stdin")
            return 2
    else:
        path = Path(sys.argv[1])
        text = read_text(path)
    if not text:
        print("File not found or empty")
        return 2
    errors = validate(text)
    if errors:
        print("VALIDATION FAILED")
        for err in errors:
            print(f"- {err}")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
