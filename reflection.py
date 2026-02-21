"""
reflection.py

Handles:
- Reviewing generated assignment
- Sending reflection prompt
- Validating reflection structure
- Returning corrected assignment JSON
"""

from typing import Dict, Any

from openai import OpenAI

from models import (
    safe_json_load,
    validate_reflection_structure,
    validate_assignment_structure
)

from utils.file_utils import load_prompt_template


class AssignmentReflector:
    def __init__(
        self,
        system_prompt_path: str,
        reflection_prompt_path: str,
        max_output_tokens: int = 2000
    ):
        self.client = OpenAI()
        self.system_prompt = load_prompt_template(system_prompt_path)
        self.reflection_prompt_template = load_prompt_template(
            reflection_prompt_path
        )
        self.max_output_tokens = max_output_tokens

    def reflect(
        self,
        weekly_syllabus: str,
        materials_text: str,
        student_profile: str,
        generated_assignment: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Sends assignment through reflection pass.
        Returns corrected assignment JSON.
        """

        formatted_prompt = self.reflection_prompt_template.format(
            weekly_syllabus=weekly_syllabus,
            materials_text=materials_text,
            student_profile=student_profile,
            generated_assignment=generated_assignment
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

        response = self.client.chat.completions.create(
            model="gpt-5.2",
            messages=messages,
            max_output_tokens=self.max_output_tokens
        )

        raw_output = response.choices[0].message.content

        reflection_json = safe_json_load(raw_output)

        validate_reflection_structure(reflection_json)

        corrected_assignment = reflection_json["corrected_assignment"]

        # Validate corrected structure
        validate_assignment_structure(corrected_assignment)

        return corrected_assignment
