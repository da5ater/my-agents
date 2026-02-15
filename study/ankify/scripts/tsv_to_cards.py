#!/usr/bin/env python3
import argparse
import json
import re
import sys


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


def normalize_type_label(text):
    upper = text.upper()
    for key, value in TYPE_NORMALIZATION.items():
        if key in upper:
            return value
    return ""


def main():
    parser = argparse.ArgumentParser(description="Convert TSV to cards.json.")
    parser.add_argument("--tsv", required=True, help="Path to TSV file.")
    parser.add_argument("--output", required=True, help="Path to cards.json.")
    args = parser.parse_args()

    cards = []
    with open(args.tsv, "r", encoding="utf-8") as handle:
        for index, raw_line in enumerate(handle):
            line = raw_line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            front, back, url = parts
            card_type = normalize_type_label(front)
            cards.append(
                {
                    "index": index,
                    "front": front,
                    "back": back,
                    "url": url,
                    "type": card_type,
                }
            )

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(cards, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
