#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Discover markdown notes in a directory."
    )
    parser.add_argument(
        "--input", required=True, help="Input folder containing markdown notes."
    )
    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    if not input_dir.exists():
        print(json.dumps({"error": f"Directory not found: {input_dir}"}))
        sys.exit(1)

    notes = []
    # Recursively find .md files, excluding hidden files/dirs
    for path in input_dir.rglob("*.md"):
        if any(part.startswith(".") for part in path.parts):
            continue
        notes.append(str(path))

    # Output as JSON list
    print(json.dumps(sorted(notes), indent=2))


if __name__ == "__main__":
    main()
