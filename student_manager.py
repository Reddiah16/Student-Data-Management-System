"""
student_manager.py
==================
Module containing core functions for student records management:
- Creating student records as dictionaries
- Reading records from a JSON file (handling missing files and corrupt JSON)
- Saving records to a JSON file
- Appending new records to existing data
- Searching and formatting student records
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Union

# Default path to students.json located in the same directory as this module
DEFAULT_FILE_PATH = Path(__file__).resolve().parent / "students.json"


def create_student_record(name: str, age: int, skills: List[str], cgpa: float) -> Dict[str, Any]:
    """
    Creates and returns a student information dictionary.

    Args:
        name: Name of the student.
        age: Age of the student.
        skills: List of skills.
        cgpa: Cumulative Grade Point Average.

    Returns:
        dict: Student record dictionary.
    """
    cleaned_skills = [s.strip() for s in skills if s and s.strip()]
    return {
        "name": str(name).strip(),
        "age": int(age),
        "skills": cleaned_skills,
        "cgpa": round(float(cgpa), 2)
    }


def load_students(filepath: Union[str, Path] = DEFAULT_FILE_PATH) -> List[Dict[str, Any]]:
    """
    Reads existing student records from the JSON file.

    Handles:
    - Missing file (FileNotFoundError): Returns an empty list without crashing.
    - Invalid/corrupt JSON (json.JSONDecodeError): Logs a warning and returns an empty list.
    - Empty file content: Handled gracefully and returns an empty list.
    - Unexpected schema (e.g. root is not a list): Returns an empty list.

    Args:
        filepath: Path to the JSON data file.

    Returns:
        list: List of student dictionaries.
    """
    file_path = Path(filepath)

    if not file_path.exists():
        print(f"[Notice] File '{file_path.name}' not found. Starting with an empty record list.")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                print(f"[Notice] File '{file_path.name}' is empty. Returning empty record list.")
                return []
            data = json.loads(content)

            if not isinstance(data, list):
                print(f"[Warning] Invalid format in '{file_path.name}'. Expected a JSON list, but got {type(data).__name__}.")
                return []

            return data

    except FileNotFoundError:
        print(f"[Notice] File '{file_path.name}' does not exist.")
        return []
    except json.JSONDecodeError as e:
        print(f"[Warning] Invalid JSON in '{file_path.name}': {e}. Returning empty record list.")
        return []
    except Exception as e:
        print(f"[Error] Unexpected error reading '{file_path.name}': {e}")
        return []


def save_students(students: List[Dict[str, Any]], filepath: Union[str, Path] = DEFAULT_FILE_PATH) -> bool:
    """
    Saves the entire list of student records into the specified JSON file.

    Args:
        students: List of student dictionaries.
        filepath: Destination path for the JSON file.

    Returns:
        bool: True if saving succeeded, False otherwise.
    """
    file_path = Path(filepath)

    try:
        # Ensure parent directories exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=4, ensure_ascii=False)
        return True

    except Exception as e:
        print(f"[Error] Failed to save students to '{file_path}': {e}")
        return False


def append_student(student: Dict[str, Any], filepath: Union[str, Path] = DEFAULT_FILE_PATH) -> bool:
    """
    Appends a new student record to the existing records in the JSON file.

    Args:
        student: Dictionary containing the student's details.
        filepath: Destination path for the JSON file.

    Returns:
        bool: True if append and save succeeded, False otherwise.
    """
    # 1. Read existing records
    records = load_students(filepath)

    # 2. Append the new record
    records.append(student)

    # 3. Save back to the JSON file
    return save_students(records, filepath)


def search_students(query: str, filepath: Union[str, Path] = DEFAULT_FILE_PATH) -> List[Dict[str, Any]]:
    """
    Searches for students whose name or skills contain the given query string.

    Args:
        query: Case-insensitive search string.
        filepath: Path to the JSON data file.

    Returns:
        list: Matching student records.
    """
    records = load_students(filepath)
    q = query.strip().lower()
    matches = []

    for s in records:
        name_match = q in str(s.get("name", "")).lower()
        skills_match = any(q in str(skill).lower() for skill in s.get("skills", []))
        if name_match or skills_match:
            matches.append(s)

    return matches


def format_student(student: Dict[str, Any]) -> str:
    """
    Returns a human-readable formatted string for a student record.
    """
    name = student.get("name", "N/A")
    age = student.get("age", "N/A")
    cgpa = student.get("cgpa", "N/A")
    skills = student.get("skills", [])
    skills_str = ", ".join(skills) if skills else "None"

    return f"Name: {name:<18} | Age: {age:<3} | CGPA: {cgpa:<5} | Skills: {skills_str}"

