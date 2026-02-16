#!/usr/bin/env python3
import argparse
import sys
import re
import urllib.parse
from typing import List, Tuple, Optional

# --- Manifesto Constants ---
BANNED_BACK_PHRASES = [
    "leads to incorrect behavior",
    "focuses on its own role",
    "not just a synonym",
    "end-to-end",
    "misused",
]

BANNED_FRONT_PATTERNS = [
    re.compile(r"^explain ", re.IGNORECASE),
    re.compile(r"^what is ", re.IGNORECASE),  # Unless anchored (checked later)
    re.compile(r"^write the code example for", re.IGNORECASE),
]

def clean_field(text: str) -> str:
    """Normalize field content: remove newlines, tabs, and trim."""
    text = text.replace("\n", "<br>").replace("\r", "")
    text = text.replace("\t", "    ")
    return text.strip()

def repair_line(line: str, vault: str, default_file: str) -> Optional[str]:
    """
    Attempt to repair a malformed TSV line.
    Target: FRONT <tab> BACK <tab> URL
    """
    # 1. Split by tab
    parts = line.strip().split("\t")
    
    # Init fields
    front = ""
    back = ""
    url = ""

    # 2. Heuristic Field Assignment
    if len(parts) == 3:
        front, back, url = parts
    elif len(parts) == 2:
        # Missing URL? or Extra tab in content?
        # Check if 2nd part looks like a URL
        if "obsidian://" in parts[1]: 
             # We have Content and URL. Content might be "Front<br>Back" if it was multi-line.
             content = parts[0]
             url = parts[1]
             
             if "<br>" in content:
                 # Heuristic: The first line was Front, the rest was Back.
                 split_content = content.split("<br>", 1)
                 front = split_content[0]
                 back = split_content[1]
             else:
                 # Truly missing back?
                 front = content
                 back = " [MISSING ANSWER] " 
             
        front = parts[0]
        back = parts[1]
        # Infer URL later
    elif len(parts) > 3:
        # Too many tabs. Assume they belong in BACK (code blocks often have tabs)
        front = parts[0]
        url = parts[-1] 
        # Check if last part is actually a URL
        if "obsidian://" in url:
            back = "    ".join(parts[1:-1])
        else:
            # Huge mess. fallback:
            # Front / Back / ... / ... 
            # We can't safely repair if we don't know where URL is.
            return None
    else:
        # 1 part? Garbage.
        return None

    # 3. Clean Content
    front = clean_field(front)
    back = clean_field(back)
    url = url.strip()

    # 4. URL Repair/Inference
    if not url or "obsidian://" not in url:
        # Infer from context
        if default_file:
             # Construct URL: obsidian://open?vault=mohamed&file={encoded_path}
             # Removing .md extension if present
             clean_path = default_file.replace(".md", "")
             encoded_path = urllib.parse.quote(clean_path)
             url = f"obsidian://open?vault={vault}&file={encoded_path}"
        else:
            return None # Cannot infer

    # 5. Fix misplaced URL (if it ended up in back somehow, though logic above handles split)
    
    # 6. Final checks
    if not front or not back:
        return None
        
    return f"{front}\t{back}\t{url}"

def validate_content(front: str, back: str) -> List[str]:
    failures = []
    
    # Banned Phrases
    for phrase in BANNED_BACK_PHRASES:
        if phrase in back.lower():
            failures.append(f"Banned phrase in back: '{phrase}'")
            
    for pattern in BANNED_FRONT_PATTERNS:
        if pattern.search(front):
            failures.append("Generic front pattern detected (e.g. 'Explain X')")

    return failures

def process_stream(input_stream, output_stream, vault="mohamed", default_file=""):
    """
    Read lines from input_stream (TSV rows), repair, validate, and write to output_stream.
    Handles multi-line broken records by buffering until a URL is found.
    """
    lines_processed = 0
    lines_valid = 0
    
    buffer = []
    
    for line in input_stream:
        line = line.replace("\r", "") # Kill CR
        # Don't strip yet, we might need trailing context if it was split? 
        # Actually safer to strip leading/trailing whitespace from the *chunk*, but internal newlines matter.
        
        buffer.append(line)
        
        # Heuristic: Does this line end with a valid-looking Obsidian URL?
        # or does the joined buffer look like it has a URL?
        joined = "".join(buffer).strip()
        
        # Check if we have a URL at the end of the buffer
        # This is a bit risky if the URL is split, but URLs usually don't contain spaces/newlines 
        # unless they are the *end* of the record.
        # TSV standard: URL is last column.
        
        # Let's try to detect the URL pattern.
        # Pattern: obsidian://open?vault=...
        if "obsidian://open?" in line or "obsidian://vault/" in line:
            # We found a terminator. Process the buffer.
            # But wait, what if the URL is in the middle? (Unlikely for the last col)
            # Assuming URL is the last thing.
            
            # Additional check: Does it look like the END of the row?
            # In the broken file, the URL is indeed at the end of the line.
            
            # Process the accumulated record
            raw_record = "".join(buffer).replace("\n", "<br>") # Join with <br> to preserve structure logic?
            # Wait, if we join with <br>, we might merging the Title and Back?
            # The original file had tabs.
            # "Front \t Back \n Back continued \t URL" -> "Front \t Back <br> Back continued \t URL"
            
            # Improve: Join buffer with "\n" first, then clean_field will handle it?
            # repair_line expects a string.
            
            # Let's re-join with a marker or just pass the raw concatenated string?
            # If we raw concat, "Back\nContinued" becomes "Back\nContinued".
            # repair_line splits by \t.
            
            full_line = "".join(buffer) 
            # Note: buffer contents include the \n from the file iteration usually? 
            # for line in file includes \n.
            
            repaired = repair_line(full_line, vault, default_file)
            
            if repaired:
                output_stream.write(repaired + "\n")
                lines_valid += 1
            else:
                 sys.stderr.write(f"Record finishing at line {lines_processed} rejected.\n")
            
            buffer = [] # Reset
            
        lines_processed += 1
        
    # Handle leftover buffer?
    if buffer:
        full_line = "".join(buffer)
        if full_line.strip():
            repaired = repair_line(full_line, vault, default_file)
            if repaired:
                output_stream.write(repaired + "\n")
                lines_valid += 1
            else:
                 sys.stderr.write(f"Leftover buffer rejected.\n")

    return lines_valid

def main():
    parser = argparse.ArgumentParser(description="Ankify TSV Validator & Repair")
    parser.add_argument("--vault", default="mohamed", help="Target vault name")
    parser.add_argument("--default-file", help="Default file path for URL inference")
    parser.add_argument("--stream", action="store_true", help="Read from stdin, write to stdout")
    # Legacy file mode support for compatibility if needed, but we prefer stream
    parser.add_argument("--input", help="Input file")
    parser.add_argument("--output", help="Output file")

    args = parser.parse_args()
    
    # Determine I/O
    if args.stream or not args.input:
        f_in = sys.stdin
        f_out = sys.stdout
    else:
        f_in = open(args.input, "r", encoding="utf-8")
        f_out = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout

    try:
        valid_count = process_stream(f_in, f_out, args.vault, args.default_file or "")
        sys.stderr.write(f"Validation complete. Valid cards: {valid_count}\n")
    finally:
        if args.input and f_in is not sys.stdin:
            f_in.close()
        if args.output and f_out is not sys.stdout:
            f_out.close()

if __name__ == "__main__":
    main()
