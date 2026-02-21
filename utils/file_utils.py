"""
utils/file_utils.py

Utility functions for file operations in Syllabic.

Responsibilities:
- Reading markdown files
- Loading prompt templates
- Writing structured JSON outputs
- Managing generated assignment folders
- Appending assignments to student profiles
- Loading all student profiles
"""

from pathlib import Path
from typing import Dict, Any
import json


# ==========================================================
# Basic Readers
# ==========================================================

def read_markdown_file(path: str) -> str:
    """
    Reads a markdown file and returns its contents as a string.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {path}")

    return file_path.read_text(encoding="utf-8")


def load_prompt_template(path: str) -> str:
    """
    Loads a prompt template from the prompts directory.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")

    return file_path.read_text(encoding="utf-8")


# ==========================================================
# JSON Writing
# ==========================================================

def write_json_file(path: str, data: Dict[str, Any]) -> None:
    """
    Writes dictionary data to a JSON file with formatting.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ==========================================================
# Folder Management
# ==========================================================

def ensure_week_folder(base_dir: str, week_number: int) -> str:
    """
    Ensures that:
        generated_assignments/week_X/

    exists.

    Returns the folder path as a string.
    """
    week_folder = Path(base_dir) / f"week_{week_number}"
    week_folder.mkdir(parents=True, exist_ok=True)
    return str(week_folder)


# ==========================================================
# Profile Update Logic
# ==========================================================

def append_assignment_to_profile(
    profile_path: str,
    week_number: int,
    assignment_json: Dict[str, Any]
) -> None:
    """
    Appends a generated assignment JSON block
    to the student's markdown profile.
    """

    profile_file = Path(profile_path)

    if not profile_file.exists():
        raise FileNotFoundError(f"Student profile not found: {profile_path}")

    assignment_block = f"""

## Week {week_number}

### Generated Assignment
```json
{json.dumps(assignment_json, indent=4, ensure_ascii=False)}
````

"""

```
with profile_file.open("a", encoding="utf-8") as f:
    f.write(assignment_block)
```

# ==========================================================

# Student Profile Loader

# ==========================================================

def load_all_student_profiles(directory: str) -> Dict[str, str]:
"""
Loads all .md files in the student_profiles directory.

```
Returns:
    {
        "student_name": "<markdown content>",
        ...
    }
"""
profiles_dir = Path(directory)

if not profiles_dir.exists():
    raise FileNotFoundError(
        f"Student profiles directory not found: {directory}"
    )

profiles: Dict[str, str] = {}

for file_path in profiles_dir.glob("*.md"):
    student_name = file_path.stem
    profiles[student_name] = file_path.read_text(encoding="utf-8")

return profiles
