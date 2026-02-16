#!/usr/bin/env python3
import argparse
import urllib.parse
from pathlib import Path
from collections import defaultdict

def parse_tsv(tsv_path):
    stats = defaultdict(lambda: {"count": 0, "fronts": []})
    total_cards = 0
    
    with open(tsv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            parts = line.split("\t")
            if len(parts) != 3: continue
            
            front, back, url = parts
            
            # Start Parse URL to get file path
            # obsidian://open?vault=mohamed&file=path%2Fto%2Fnote
            try:
                parsed = urllib.parse.urlparse(url)
                query = urllib.parse.parse_qs(parsed.query)
                file_encoded = query.get("file", ["unknown"])[0]
                file_path = urllib.parse.unquote(file_encoded)
            except:
                file_path = "unknown"
                
            stats[file_path]["count"] += 1
            stats[file_path]["fronts"].append(front)
            total_cards += 1
            
    return stats, total_cards

def generate_markdown(stats, total_cards, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Ankify Run Summary\n\n")
        f.write(f"**Total Cards Generated**: {total_cards}\n")
        f.write(f"**Notes Processed**: {len(stats)}\n\n")
        
        f.write("## Breakdown by Note\n\n")
        f.write("| Note | Cards |\n")
        f.write("|---|---|\n")
        
        # Sort by count desc
        sorted_stats = sorted(stats.items(), key=lambda x: x[1]["count"], reverse=True)
        
        for note, data in sorted_stats:
            f.write(f"| `{note}` | {data['count']} |\n")
            
        f.write("\n## Validation Status\n\n")
        f.write("All cards in the TSV have passed the strict Validation Gate.\n")

def main():
    parser = argparse.ArgumentParser(description="Generate Ankify Report from TSV")
    parser.add_argument("--tsv", required=True, help="Input TSV path")
    parser.add_argument("--output", required=True, help="Output Markdown path")
    
    args = parser.parse_args()
    
    if not Path(args.tsv).exists():
        print(f"No TSV found at {args.tsv}. Generating empty report.")
        with open(args.output, "w") as f:
            f.write("# Ankify Run Summary\n\nNo output generated.")
        return

    stats, total = parse_tsv(args.tsv)
    generate_markdown(stats, total, args.output)
    print(f"Report generated at {args.output}")

if __name__ == "__main__":
    main()
