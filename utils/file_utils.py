"""
utils/file_utils.py

Handles:
- Reading markdown files
- Writing JSON files
- Appending generated assignments to student profiles
- Creating week-specific folders
- Loading prompt templates
"""

import os
import json
from pathlib import Path
from typing import Dict, Any


# =========================
# Basic File Readers
# =========================

def read_markdown_file(path: str) -> str:
    """Reads a markdown file and returns its content as string."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_prompt_template(path: str) -> str:
    """Loads a prompt template from prompts directory."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# =========================
# JSON Writing
# =========================

def write_json_file(path: str, data: Dict[str, Any]) -> None:
    """Writes dictionary to JSON file with formatting."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# =========================
# Folder Management
# =========================

def ensure_week_folder(base_dir: str, week_number: int) -> str:
    """
    Ensures generated_assignments/week_X exists.
    Returns full path to folder.
    """
    week_folder = Path(base_dir) / f"week_{week_number}"
    week_folder.mkdir(parents=True, exist_ok=True)
    return str(week_folder)


# =========================
# Profile Update Logic
# =========================

def append_assignment_to_profile(
    profile_path: str,
    week_number: int,
    assignment_json: Dict[str, Any]
) -> None:
    """
    Appends generated assignment JSON to the student's markdown profile.
    """

    assignment_block = f"""

## Week {week_number}

### Generated Assignment
```json
{json.dumps(assignment_json, indent=4, ensure_ascii=False)}
