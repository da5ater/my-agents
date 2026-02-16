#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
import datetime
from pathlib import Path

# --- Configuration ---
VAULT_NAME = "mohamed"
OUTPUT_FILENAME = "ankify_output.tsv"

def get_run_id(corpus_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    safe_name = corpus_path.name.replace(" ", "_")
    return f"{timestamp}_{safe_name}"

def save_manifest(manifest, manifest_path):
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Process corpus through Ankify Manifesto Compiler.")
    parser.add_argument("--input", required=True, help="Input folder containing markdown notes.")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen without running.")
    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    script_dir = Path(__file__).parent.resolve()

    # 1. Setup Run Workspace
    run_id = get_run_id(input_dir)
    run_workspace = Path("Ankyfy Folders") / run_id
    
    if not args.dry_run:
        run_workspace.mkdir(parents=True, exist_ok=True)
        # Initialize Output Stream
        output_tsv_path = input_dir / OUTPUT_FILENAME
        # We append, but if it's a new run invocation, maybe we should backup old?
        # For now, let's assume we want to append or create new.
        # Use 'a' mode (append)
        print(f"Streaming output to: {output_tsv_path}")

    print(f"Run Workspace: {run_workspace.resolve()}")

    # 2. Discover Notes
    notes = []
    for path in input_dir.rglob("*.md"):
        if "Ankyfy Folders" in path.parts: continue
        if any(part.startswith(".") for part in path.parts): continue
        notes.append(path)

    print(f"Discovered {len(notes)} notes.")
    
    if args.dry_run:
        return

    # 3. Process Stream
    manifest = []
    
    # We open the output stream in append mode.
    # We rely on the Agent (LLM) to generate content via the SKILL.md prompt.
    # BUT, this script is supposed to drive the process?
    # Wait, the user prompt implies: "Process: per-note analysis -> per-note card plan -> card generation -> Output: a single TSV stream"
    # This implies this script should orchestrate the LLM?
    # ACTUALLY, the current architecture relies on the USER (Agent) running tools.
    # This script is likely a helper the AGENT calls, OR the Agent *is* the pipeline.
    # The `process_corpus.py` script was previously calling `generate_ankify_tsv.py`.
    # Now, `generate_ankify_tsv.py` is legacy.
    # The AGENT (me) is replacing the Generator Script.
    # SO, this script might just be for *reporting* or *finalizing*?
    
    # REVIEWING THE PLAN: 
    # "Refactor process_corpus.py to support Streaming Mode... Iteration: Discover note -> (Agent performs Internalization/Planning/Generation) -> Append valid cards"
    # Wait, the Python script cannot invoke the LLM Agent. The Python script IS the tool the Agent calls.
    # OR, the Agent calls `process_corpus.py` which calls... what?
    
    # CORRECTION: The User's request implies the SYSTEM (Agent + Scripts) acts like a compiler.
    # If I am the Agent, I *am* the compiler using tools.
    # `process_corpus.py` might be useful to *enumerate* notes for me?
    # OR, maybe the user expects `process_corpus.py` to be the entry point script they run?
    # If so, `process_corpus.py` needs to call an LLM API?
    # NO, the user said "LLM-driven generation with script-based validation".
    # Typically this means the Agent (Model) runs the loop.
    # BUT `process_corpus.py` is a script.
    
    # Let's look at `workflow.md`:
    # "1. Parse... 2. Internalize (LLM)... 3. Plan (LLM)... 4. Generate (LLM)... 5. Validate (Script)"
    
    # If the user runs `process_corpus.py` from the terminal, it cannot perform steps 2, 3, 4 unless it calls an LLM API.
    # The existing `process_corpus.py` called `generate_ankify_tsv.py` (regex).
    
    # RE-READING SKILL.md (implied): "The Agent (User Session) IS the runner."
    # So `process_corpus.py` might effectively be dead or just a "Discovery + Validation" harness?
    # "Output strategy: streaming TSV... One ankify_output.tsv at the root... Process notes iteratively: analyze → generate cards → validate → append rows immediately"
    
    # If the Agent is doing the work manually, `process_corpus.py` isn't needed for *generation*.
    # BUT, the user might want a script to *orchestrate* validation and appending if the Agent generates a block of text?
    
    # Let's assume `process_corpus.py` is now a "Manager" script that:
    # 1. Discovers notes.
    # 2. (Maybe) Tracks progress?
    # 3. Validates & Appends content provided to it?
    
    # Actually, the user's plan said: "Refactor process_corpus.py to support Streaming Mode... Discovery... Append valid cards".
    # It seems `process_corpus.py` is intended to be the *harness*.
    # But without an LLM call inside it, it can't generate.
    
    # HYPOTHESIS: The User (Agent) will run `process_corpus.py`? No, the *User* (Human) asks the *Agent* (Me) to run it.
    # If I am the Agent, I can read files and generate cards.
    # `process_corpus.py` might be better suited as a "Bulk Validator/Merger" or it's deprecated?
    # "Delete legacy artifacts... Refactor process_corpus.py"
    
    # Let's make `process_corpus.py` a "Stub" that allows the Agent to say "I am processing file X", and then the Agent calls `validate_cards.py --stream`?
    # Or maybe the Agent just writes directly to `ankify_output.tsv`?
    
    # Let's look at the Task again: "Refactor process_corpus.py to support Streaming Mode".
    # Maybe it just sets up the stream and handles the "Validate -> Append" part?
    # i.e., It accepts raw TSV from stdin (generated by Agent?) and appends it?
    
    # Let's reimagine `process_corpus.py` as `stream_cards.py`:
    # usage: `process_corpus.py --note "path/to/note.md" --content "FRONT\tBACK\tURL"`
    # No, that's tedious.
    
    # WAIT. The SKILL.md prompt implies the AGENT follows the workflow.
    # "Process: per-note analysis -> per-note card plan -> card generation"
    # This happens in the CHAT.
    # So `process_corpus.py` is likely NOT the main driver anymore.
    # It might be used for "Batch Validation" or "Final Report".
    
    # HOWEVER, the implementation plan explicitly says:
    # "Refactor process_corpus.py... Streaming Mode: Initialize ankify_output.tsv... Iteration: Discover note... Append valid cards"
    
    # If `process_corpus.py` iterates notes, it needs to generate cards.
    # Since it can't (no LLM), maybe it's just a shell that *would* call a generator if one existed?
    # OR, maybe I should strip `process_corpus.py` down to just being a "Discovery & Reporting" tool, and the "Generation" loop happens via the Agent calling a different tool?
    
    # Let's assume the AGENT runs the loop manually in the chat:
    # 1. Agent runs `ls -R` (or similar) to find notes.
    # 2. Agent picks a note.
    # 3. Agent reads note.
    # 4. Agent generates cards (internally).
    # 5. Agent calls `validate_cards.py --stream` (input=cards) -> `ankify_output.tsv`.
    
    # In this case, `process_corpus.py` is indeed mostly dead/legacy, or just a "Batch Health Check".
    # BUT I promised to refactor it.
    # I will modify it to be a "Workspace Initializer + Finalizer" and maybe a "Progress Tracker".
    # It will NOT generate cards.
    
    pass

if __name__ == "__main__":
    main()
