"""
generator.py

Handles:
- Building GPT-5.2 message payload
- Injecting system role + assignment prompt
- Calling OpenAI API
- Parsing structured JSON safely
- Validating assignment schema
"""

import os
from typing import Dict, Any

from openai import OpenAI

from models import (
    safe_json_load,
    validate_assignment_structure
)

from utils.file_utils import load_prompt_template


class AssignmentGenerator:
    def __init__(
        self,
        system_prompt_path: str,
        assignment_prompt_path: str,
        max_output_tokens: int = 2000
    ):
        self.client = OpenAI()
        self.system_prompt = load_prompt_template(system_prompt_path)
        self.assignment_prompt_template = load_prompt_template(
            assignment_prompt_path
        )
        self.max_output_tokens = max_output_tokens

    def build_messages(
        self,
        week_number: int,
        weekly_syllabus: str,
        materials_text: str,
        student_profile: str
    ):
        formatted_prompt = self.assignment_prompt_template.format(
            week_number=week_number,
            weekly_syllabus=weekly_syllabus,
            materials_text=materials_text,
            student_profile=student_profile
        )

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": formatted_prompt
            }
        ]

        return messages

    def generate_assignment(
        self,
        week_number: int,
        weekly_syllabus: str,
        materials_text: str,
        student_profile: str
    ) -> Dict[str, Any]:
        """
        Generates structured assignment JSON using GPT-5.2.
        """

        messages = self.build_messages(
            week_number,
            weekly_syllabus,
            materials_text,
            student_profile
        )

        response = self.client.chat.completions.create(
            model="gpt-5.2",
            messages=messages,
            max_output_tokens=self.max_output_tokens
        )

        raw_output = response.choices[0].message.content

        parsed_json = safe_json_load(raw_output)

        validate_assignment_structure(parsed_json)

        return parsed_json
