#!/usr/bin/env python3
import argparse
import json
import math
import re
import sys


TYPE_PRIORITY = [
    "SYNTHESIS",
    "MODEL",
    "FAILURE_MODE",
    "NEGATION",
    "COUNTER_EVIDENCE",
    "CONSTRUCTIVE",
    "THEORY",
    "DEFINITION",
    "PROCEDURE",
]


def strip_html(text):
    return re.sub(r"<[^>]+>", "", text)


def normalize_front(front):
    text = strip_html(front)
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text):
    return re.findall(r"[a-z0-9_]+", text)


def cosine_similarity(a_tokens, b_tokens):
    a_freq = {}
    b_freq = {}
    for token in a_tokens:
        a_freq[token] = a_freq.get(token, 0) + 1
    for token in b_tokens:
        b_freq[token] = b_freq.get(token, 0) + 1
    dot = 0
    for token, count in a_freq.items():
        dot += count * b_freq.get(token, 0)
    a_norm = math.sqrt(sum(v * v for v in a_freq.values()))
    b_norm = math.sqrt(sum(v * v for v in b_freq.values()))
    if a_norm == 0 or b_norm == 0:
        return 0.0
    return dot / (a_norm * b_norm)


def token_overlap(a_tokens, b_tokens):
    if not a_tokens:
        return 0.0
    a_set = set(a_tokens)
    b_set = set(b_tokens)
    return len(a_set.intersection(b_set)) / max(1, len(a_set))


def type_rank(card_type):
    try:
        return TYPE_PRIORITY.index(card_type)
    except ValueError:
        return len(TYPE_PRIORITY)


def main():
    parser = argparse.ArgumentParser(
        description="Detect redundant cards and propose pruning."
    )
    parser.add_argument("--cards", required=True, help="Path to cards JSON list.")
    parser.add_argument("--output", required=True, help="Path to prune plan JSON.")
    parser.add_argument("--threshold-cosine", type=float, default=0.92)
    parser.add_argument("--threshold-overlap", type=float, default=0.85)
    args = parser.parse_args()

    with open(args.cards, "r", encoding="utf-8") as handle:
        cards = json.load(handle)

    candidates = []
    for index, card in enumerate(cards):
        front = card.get("front", "")
        normalized = normalize_front(front)
        tokens = tokenize(normalized)
        candidates.append(
            {
                "index": index,
                "front": front,
                "normalized": normalized,
                "tokens": tokens,
                "type": card.get("type", ""),
                "url": card.get("url", ""),
            }
        )

    prune = []
    redundancy = []

    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            a = candidates[i]
            b = candidates[j]
            if a["url"] != b["url"]:
                continue
            cosine = cosine_similarity(a["tokens"], b["tokens"])
            overlap = token_overlap(a["tokens"], b["tokens"])
            if cosine >= args.threshold_cosine or overlap >= args.threshold_overlap:
                redundancy.append(
                    {
                        "a_index": a["index"],
                        "b_index": b["index"],
                        "cosine": cosine,
                        "overlap": overlap,
                    }
                )
                a_rank = type_rank(a["type"])
                b_rank = type_rank(b["type"])
                if a_rank == b_rank:
                    drop_index = b["index"]
                elif a_rank < b_rank:
                    drop_index = b["index"]
                else:
                    drop_index = a["index"]
                prune.append(
                    {
                        "drop_index": drop_index,
                        "reason": "redundant",
                    }
                )

    output = {
        "redundancy_report": redundancy,
        "prune_plan": prune,
    }

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(output, handle, indent=2)

    return 0


if __name__ == "__main__":
    sys.exit(main())
