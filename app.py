"""
app.py

Main orchestration engine for Syllabic.

Pipeline:
- Parse syllabus
- Extract selected week section
- Extract relevant material filenames
- Load relevant materials
- Load student profiles
- Generate assignment
- Run reflection
- Save JSON
- Append to student profile
"""

import os
from pathlib import Path
from typing import Dict

from parser import (
    extract_syllabus_text,
    extract_week_section,
    extract_material_filenames,
    load_relevant_materials
)

from generator import AssignmentGenerator
from reflection import AssignmentReflector

from utils.file_utils import (
    load_all_student_profiles,
    ensure_week_folder,
    write_json_file,
    append_assignment_to_profile
)


# =========================
# Configuration
# =========================

BASE_DIR = Path(__file__).parent

SYLLABUS_PATH = BASE_DIR / "syllabus" / "syllabus.pdf"
COURSE_MATERIALS_DIR = BASE_DIR / "course_materials"
STUDENT_PROFILES_DIR = BASE_DIR / "student_profiles"
GENERATED_ASSIGNMENTS_DIR = BASE_DIR / "generated_assignments"

SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system_role.txt"
ASSIGNMENT_PROMPT_PATH = BASE_DIR / "prompts" / "assignment_prompt.txt"
REFLECTION_PROMPT_PATH = BASE_DIR / "prompts" / "reflection_prompt.txt"


# =========================
# Main Engine
# =========================

class SyllabicEngine:

    def __init__(self):
        self.generator = AssignmentGenerator(
            system_prompt_path=str(SYSTEM_PROMPT_PATH),
            assignment_prompt_path=str(ASSIGNMENT_PROMPT_PATH)
        )

        self.reflector = AssignmentReflector(
            system_prompt_path=str(SYSTEM_PROMPT_PATH),
            reflection_prompt_path=str(REFLECTION_PROMPT_PATH)
        )

    def generate_for_week(self, week_number: int):
        print(f"\n=== Generating assignments for Week {week_number} ===\n")

        # 1️⃣ Extract syllabus text
        syllabus_text = extract_syllabus_text(str(SYLLABUS_PATH))

        # 2️⃣ Extract week section
        weekly_section = extract_week_section(syllabus_text, week_number)

        # 3️⃣ Extract mentioned material filenames
        material_filenames = extract_material_filenames(weekly_section)

        # 4️⃣ Load relevant materials
        materials_text = load_relevant_materials(
            str(COURSE_MATERIALS_DIR),
            material_filenames
        )

        # 5️⃣ Load student profiles
        student_profiles = load_all_student_profiles(
            str(STUDENT_PROFILES_DIR)
        )

        # 6️⃣ Ensure week output folder
        week_folder = ensure_week_folder(
            str(GENERATED_ASSIGNMENTS_DIR),
            week_number
        )

        # 7️⃣ Process each student
        for student_name, profile_text in student_profiles.items():

            print(f"Processing student: {student_name}")

            # Generate assignment
            assignment_json = self.generator.generate_assignment(
                week_number=week_number,
                weekly_syllabus=weekly_section,
                materials_text=materials_text,
                student_profile=profile_text
            )

            # Reflection pass
            corrected_assignment = self.reflector.reflect(
                weekly_syllabus=weekly_section,
                materials_text=materials_text,
                student_profile=profile_text,
                generated_assignment=assignment_json
            )

            # Save JSON file
            output_path = Path(week_folder) / f"{student_name}.json"
            write_json_file(str(output_path), corrected_assignment)

            # Append to profile
            profile_path = Path(STUDENT_PROFILES_DIR) / f"{student_name}.md"
            append_assignment_to_profile(
                str(profile_path),
                week_number,
                corrected_assignment
            )

            print(f"Finished: {student_name}")

        print("\n=== Week generation complete ===\n")
