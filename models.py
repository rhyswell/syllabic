"""
models.py

Defines:
- Assignment JSON schema
- Reflection JSON schema
- Validation helpers
- Dataclasses for structured handling
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
import json


# =========================
# Dataclasses
# =========================

@dataclass
class AssignmentDetails:
    title: str
    description: str
    deliverables: List[str]
    evaluation_criteria: List[str]


@dataclass
class AssignmentOutput:
    week: int
    topic: str
    learning_objectives: List[str]
    assignment: AssignmentDetails
    reading_list: List[str]
    difficulty_level: str
    personalization_rationale: str


@dataclass
class ReflectionOutput:
    is_valid: bool
    issues_found: List[str]
    corrected_assignment: Dict[str, Any]


# =========================
# Required JSON Structure
# =========================

REQUIRED_ASSIGNMENT_KEYS = {
    "week",
    "topic",
    "learning_objectives",
    "assignment",
    "reading_list",
    "difficulty_level",
    "personalization_rationale"
}

REQUIRED_ASSIGNMENT_SUBKEYS = {
    "title",
    "description",
    "deliverables",
    "evaluation_criteria"
}

REQUIRED_REFLECTION_KEYS = {
    "is_valid",
    "issues_found",
    "corrected_assignment"
}


# =========================
# Validation Helpers
# =========================

def validate_assignment_structure(data: Dict[str, Any]) -> bool:
    """
    Validates that the assignment JSON follows the required schema.
    Raises ValueError if invalid.
    """

    missing_keys = REQUIRED_ASSIGNMENT_KEYS - data.keys()
    if missing_keys:
        raise ValueError(f"Missing assignment keys: {missing_keys}")

    assignment_block = data.get("assignment", {})
    missing_subkeys = REQUIRED_ASSIGNMENT_SUBKEYS - assignment_block.keys()
    if missing_subkeys:
        raise ValueError(f"Missing assignment subkeys: {missing_subkeys}")

    if not isinstance(data["learning_objectives"], list):
        raise ValueError("learning_objectives must be a list")

    if not isinstance(data["reading_list"], list):
        raise ValueError("reading_list must be a list")

    if not isinstance(assignment_block["deliverables"], list):
        raise ValueError("deliverables must be a list")

    if not isinstance(assignment_block["evaluation_criteria"], list):
        raise ValueError("evaluation_criteria must be a list")

    return True


def validate_reflection_structure(data: Dict[str, Any]) -> bool:
    """
    Validates reflection output structure.
    """

    missing_keys = REQUIRED_REFLECTION_KEYS - data.keys()
    if missing_keys:
        raise ValueError(f"Missing reflection keys: {missing_keys}")

    if not isinstance(data["is_valid"], bool):
        raise ValueError("is_valid must be boolean")

    if not isinstance(data["issues_found"], list):
        raise ValueError("issues_found must be a list")

    if not isinstance(data["corrected_assignment"], dict):
        raise ValueError("corrected_assignment must be a dictionary")

    return True


# =========================
# Safe JSON Loader
# =========================

def safe_json_load(raw_text: str) -> Dict[str, Any]:
    """
    Safely loads model output as JSON.
    Strips potential markdown fences if present.
    """

    cleaned = raw_text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]

    return json.loads(cleaned)
