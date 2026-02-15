#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Process corpus through Ankify pipeline."
    )
    parser.add_argument(
        "--input", required=True, help="Input folder containing markdown notes."
    )
    parser.add_argument(
        "--output", required=True, help="Output path for the unified TSV."
    )
    parser.add_argument("--vault", required=True, help="Vault name for Obsidian URLs.")
    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    output_file = Path(args.output).resolve()
    work_dir = input_dir / "ankify_work"
    work_dir.mkdir(exist_ok=True)

    script_dir = Path(__file__).parent.resolve()

    # 1. Discover Notes
    notes = []
    for path in input_dir.rglob("*.md"):
        if "ankify_work" in path.parts or ".obsidian" in path.parts:
            continue
        notes.append(path)

    print(f"Discovered {len(notes)} notes.")

    manifest = []
    valid_tsvs = []

    # 2. Process Each Note
    for note in notes:
        # Determine paths
        rel_path = note.relative_to(input_dir)
        safe_name = str(rel_path).replace("/", "_").replace(" ", "_").replace(".md", "")
        note_tsv = work_dir / f"{safe_name}.tsv"

        print(f"Processing: {note.name} -> {note_tsv.name}")

        # A. Generate Initial TSV
        cmd_gen = [
            sys.executable,
            str(script_dir / "generate_ankify_tsv.py"),
            "--input",
            str(note),
            "--output",
            str(note_tsv),
            "--vault",
            args.vault,
        ]
        res_gen = subprocess.run(cmd_gen, capture_output=True, text=True)
        if res_gen.returncode != 0:
            print(f"  Generation FAILED for {note.name}")
            print(res_gen.stderr)
            continue

        # B. Run Enforcement Loop
        cmd_loop = [
            str(script_dir / "run_ankify_checks_loop.sh"),
            str(note),
            str(note_tsv),
        ]
        # We allow the loop to control its own output/exit
        res_loop = subprocess.run(cmd_loop, capture_output=True, text=True)

        # Check if TSV is valid (non-empty and exists)
        if note_tsv.exists() and note_tsv.stat().st_size > 0:
            manifest.append({"note": str(note), "tsv": str(note_tsv)})
            valid_tsvs.append(note_tsv)
            status = "PASS" if res_loop.returncode == 0 else "WARN (Best Effort)"
            print(f"  Loop Finished: {status}")
        else:
            print(f"  Loop Failed: No TSV produced for {note.name}")
            if res_loop.stderr:
                print(res_loop.stderr[:200])

    # 3. Generate Reports
    manifest_path = work_dir / "manifest.json"
    run_stats_path = work_dir / "run_stats.json"
    run_summary_path = input_dir / "run_summary.md"
    manifesto_report_path = input_dir / "manifesto_actualization_report.md"

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Generating reports...")
    cmd_reports = [
        sys.executable,
        str(script_dir / "run_ankify_folder_checks.py"),
        "--manifest",
        str(manifest_path),
        "--run-stats",
        str(run_stats_path),
        "--summary-output",
        str(run_summary_path),
        "--manifesto-output",
        str(manifesto_report_path),
    ]
    subprocess.run(cmd_reports, check=True)

    # 4. Merge TSVs
    print(f"Merging {len(valid_tsvs)} TSVs into {output_file.name}...")
    with open(output_file, "w", encoding="utf-8") as outfile:
        for tsv_path in valid_tsvs:
            with open(tsv_path, "r", encoding="utf-8") as infile:
                shutil.copyfileobj(infile, outfile)
                # Ensure newline between files if missing
                infile.seek(0, os.SEEK_END)
                if infile.tell() > 0:
                    infile.seek(infile.tell() - 1, os.SEEK_SET)
                    if infile.read(1) != "\n":
                        outfile.write("\n")

    print("Done.")
    print(f"Outputs:\n  {output_file}\n  {run_summary_path}\n  {manifesto_report_path}")


if __name__ == "__main__":
    main()
