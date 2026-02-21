"""
parser.py

Responsible for:
- Extracting text from syllabus (PDF or DOCX)
- Extracting a specific week section (e.g., "Week 3:")
- Extracting referenced material filenames from that section
- Loading only relevant course materials
"""

import re
from pathlib import Path
from typing import List

from pypdf import PdfReader
from docx import Document


# ==========================================================
# Text Extraction
# ==========================================================

def extract_text_from_pdf(path: str) -> str:
    """
    Extracts text from a PDF file.
    """
    reader = PdfReader(path)
    text_chunks = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_chunks.append(page_text)

    return "\n".join(text_chunks)


def extract_text_from_docx(path: str) -> str:
    """
    Extracts text from a DOCX file.
    """
    doc = Document(path)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)


def extract_syllabus_text(path: str) -> str:
    """
    Detects file type (PDF or DOCX) and extracts text.
    """
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Syllabus file not found: {path}")

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return extract_text_from_pdf(str(file_path))
    elif suffix == ".docx":
        return extract_text_from_docx(str(file_path))
    else:
        raise ValueError("Unsupported syllabus format. Use PDF or DOCX.")


# ==========================================================
# Weekly Section Extraction
# ==========================================================

def extract_week_section(full_text: str, week_number: int) -> str:
    """
    Extracts a section labeled exactly as:

        Week X:

    Assumes consistent labeling and ordering.
    """

    pattern = rf"Week {week_number}:(.*?)(?=Week {week_number + 1}:|$)"
    match = re.search(pattern, full_text, flags=re.DOTALL | re.IGNORECASE)

    if not match:
        raise ValueError(f"Week {week_number} section not found in syllabus.")

    return match.group(1).strip()


# ==========================================================
# Material Filename Extraction
# ==========================================================

def extract_material_filenames(week_section: str) -> List[str]:
    """
    Extracts filenames referenced in the week section.

    Expected formats:
        chapter3.pdf
        slides_week3.pptx
        reading.docx
        notes.txt

    Returns a list of unique filenames.
    """

    pattern = r"\b[\w\-.]+\.(pdf|docx|pptx|txt)\b"

    filenames = {
        match.group(0)
        for match in re.finditer(pattern, week_section, flags=re.IGNORECASE)
    }

    return sorted(filenames)


# ==========================================================
# Course Material Loading
# ==========================================================

def load_material_text(material_path: Path) -> str:
    """
    Extracts text from a material file.
    Supports PDF, DOCX, and TXT.
    PPTX is recognized but not parsed for text.
    """

    suffix = material_path.suffix.lower()

    if suffix == ".pdf":
        return extract_text_from_pdf(str(material_path))

    if suffix == ".docx":
        return extract_text_from_docx(str(material_path))

    if suffix == ".txt":
        return material_path.read_text(encoding="utf-8")

    # PPTX and other formats not parsed for text
    return ""


def load_relevant_materials(
    materials_directory: str,
    filenames: List[str]
) -> str:
    """
    Loads and concatenates only the materials referenced
    in the weekly syllabus section.

    Returns a single combined text block.
    """

    materials_dir = Path(materials_directory)

    if not materials_dir.exists():
        raise FileNotFoundError(
            f"Course materials directory not found: {materials_directory}"
        )

    combined_sections = []

    for filename in filenames:
        material_path = materials_dir / filename

        if material_path.exists():
            material_text = load_material_text(material_path)

            if material_text.strip():
                combined_sections.append(
                    f"\n===== {filename} =====\n{material_text}"
                )
        else:
            print(f"[Warning] Referenced material not found: {filename}")

    return "\n".join(combined_sections).strip()
