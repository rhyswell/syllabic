# Syllabic

Syllabic is a Python-based AI assignment generation system that creates personalized weekly university assignments using GPT-5.2.

It is designed as a teacher-facing tool that:

* Parses a structured course syllabus (PDF/DOCX)
* Extracts weekly topics automatically
* Loads only relevant course materials referenced in the syllabus
* Reads structured student profiles (Markdown)
* Generates bespoke assignments tailored to each student
* Runs a self-reflection validation pass
* Outputs structured JSON
* Appends assignments to student history

---

## Why This Project

Syllabic demonstrates:

* Controlled long-context prompting
* Constrained knowledge usage (no external sources)
* Strict structured JSON validation
* Self-reflection loop for output correction
* Separation of prompts from logic
* File-based persistence
* Deterministic generation (no temperature)
* Modular architecture
* GUI integration

---

## System Architecture

The system follows layered architecture:

Contracts → Utilities → Parsing → LLM Layer → Reflection → Orchestration → GUI

### Core Components

**models.py**
Defines strict JSON schema and validation rules.

**parser.py**
Handles:

* PDF and DOCX syllabus parsing
* Weekly section extraction via regex
* Extraction of referenced material filenames
* Loading only relevant course materials

**generator.py**

* Uses GPT-5.2
* Uses `messages`
* Uses `max_output_tokens`
* No temperature
* Strict JSON parsing and validation

**reflection.py**
Second LLM pass that:

* Audits assignment correctness
* Checks syllabus alignment
* Checks personalization
* Enforces material-only usage
* Returns corrected JSON if needed

**app.py**
Full orchestration pipeline.

**gui.py**
Minimal Tkinter interface for week selection and execution.

---

## Assignment Generation Pipeline

1. User selects week in GUI
2. Syllabus is parsed
3. Week section is extracted
4. Referenced material filenames are identified
5. Only relevant materials are loaded
6. Each student profile is read
7. Assignment is generated via GPT-5.2
8. Reflection pass validates and corrects output
9. JSON is saved
10. Assignment is appended to student profile

The model is explicitly instructed to use only the provided syllabus and materials.

---

## Structured Output Contract

Assignments must follow:

```
{
  "week": int,
  "topic": string,
  "learning_objectives": [string],
  "assignment": {
    "title": string,
    "description": string,
    "deliverables": [string],
    "evaluation_criteria": [string]
  },
  "reading_list": [string],
  "difficulty_level": string,
  "personalization_rationale": string
}
```

## Reflection Loop

After generation, a second GPT-5.2 pass evaluates:

* Alignment with syllabus objectives
* Use of only provided materials
* Proper difficulty calibration
* Personalization quality
* Structural integrity

If issues are detected, a corrected version is returned.

---

## Deterministic LLM Usage

* Model: gpt-5.2
* No temperature parameter
* Uses `messages`
* Uses `max_output_tokens`
* Strict JSON-only responses
* Prompt templates stored separately from code

---

## Student Profile Structure

Each student profile is a structured Markdown file containing:

* About Me
* Goals
* Strengths
* Weaknesses
* Learning Preferences
* Time Availability
* Weekly History

Assignments are adapted across all dimensions.

---

## Folder Structure

```
syllabic/
│
├── app.py
├── gui.py
├── generator.py
├── parser.py
├── reflection.py
├── models.py
│
├── prompts/
│   ├── system_role.txt
│   ├── assignment_prompt.txt
│   └── reflection_prompt.txt
│
├── syllabus/
│   └── syllabus.pdf
│
├── course_materials/
│
├── student_profiles/
│
├── generated_assignments/
│
└── utils/
    └── file_utils.py
```

## Potential Extensions

* RAG pipeline with embeddings
* Automatic grading
* Progress analytics dashboard
* Skill gap detection
* Multi-agent architecture
* Web-based teacher dashboard
* Deployment via FastAPI
