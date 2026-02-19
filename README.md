# File Organizer Automation Tool

A Python automation tool that organizes files in a target folder (e.g., Downloads) into subfolders based on file type.
Includes a dry-run mode for safe preview and logging for traceability.

## Features
- Organizes files by extension using configurable rules (rules.json)
- Dry-run mode (preview moves without changing files)
- Handles duplicate filenames by auto-renaming
- Writes a log file after executing moves

## Tech Stack
- Python 3
- pathlib, shutil, json (standard library)

## How to Run (macOS)
1) (Optional) Create a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate

2) Run in dry-run mode (recommended first):
   python3 organizer.py

3) Execute actual moves:
   - Open organizer.py and set dry_run=False
   - Run again:
     python3 organizer.py

## Configuration
Edit `rules.json` to map extensions to folder names.
Example:
{
  "pdf": "PDFs",
  "png": "Images",
  "zip": "Archives"
}

## Notes
- This project was built to practice practical scripting, safe file operations, and clean code structure.
- For safety, always run dry-run mode first.
