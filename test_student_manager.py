"""
test_student_manager.py
=======================
Automated test suite verifying the requirements:
1. Creating student dictionary.
2. Saving records to JSON.
3. Reading existing records from JSON.
4. Appending new records.
5. Handling missing files.
6. Handling invalid / malformed JSON.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure day3_project directory is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from student_manager import (
    create_student_record,
    load_students,
    save_students,
    append_student,
    search_students,
    format_student,
)


class TestStudentManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for test files
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.test_dir.name) / "test_students.json"

    def tearDown(self):
        # Clean up temporary directory
        self.test_dir.cleanup()

    def test_create_student_record(self):
        """Test creating a dictionary from student details."""
        record = create_student_record(
            name="Reddiah",
            age=23,
            skills=["Python", "SQL", "AI"],
            cgpa=8.26
        )

        self.assertIsInstance(record, dict)
        self.assertEqual(record["name"], "Reddiah")
        self.assertEqual(record["age"], 23)
        self.assertEqual(record["skills"], ["Python", "SQL", "AI"])
        self.assertEqual(record["cgpa"], 8.26)

    def test_save_and_load_students(self):
        """Test saving student records to JSON and loading them back."""
        sample_students = [
            {
                "name": "Reddiah",
                "age": 23,
                "skills": ["Python", "SQL", "AI"],
                "cgpa": 8.26
            },
            {
                "name": "Anita",
                "age": 21,
                "skills": ["Java", "Docker"],
                "cgpa": 9.10
            }
        ]

        save_result = save_students(sample_students, filepath=self.test_file)
        self.assertTrue(save_result)
        self.assertTrue(self.test_file.exists())

        loaded_students = load_students(filepath=self.test_file)
        self.assertEqual(len(loaded_students), 2)
        self.assertEqual(loaded_students[0]["name"], "Reddiah")
        self.assertEqual(loaded_students[1]["cgpa"], 9.10)

    def test_append_student(self):
        """Test appending a new student record to existing records in JSON."""
        # Start with one student
        initial_student = create_student_record("Reddiah", 23, ["Python", "SQL"], 8.26)
        save_students([initial_student], filepath=self.test_file)

        # Append second student
        new_student = create_student_record("John Doe", 22, ["C++", "Linux"], 7.85)
        append_result = append_student(new_student, filepath=self.test_file)
        self.assertTrue(append_result)

        # Verify both records exist
        records = load_students(filepath=self.test_file)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["name"], "Reddiah")
        self.assertEqual(records[1]["name"], "John Doe")
        self.assertEqual(records[1]["skills"], ["C++", "Linux"])

    def test_handle_missing_file(self):
        """Test that missing JSON file returns an empty list and does not crash."""
        non_existent_file = Path(self.test_dir.name) / "does_not_exist.json"
        self.assertFalse(non_existent_file.exists())

        records = load_students(filepath=non_existent_file)
        self.assertEqual(records, [])

    def test_handle_invalid_json(self):
        """Test that corrupted / invalid JSON returns an empty list and does not crash."""
        # Write corrupted JSON
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("{ invalid_json: this is not valid, missing quotes and brackets ")

        records = load_students(filepath=self.test_file)
        self.assertEqual(records, [])

    def test_handle_empty_file(self):
        """Test that an empty file returns an empty list."""
        self.test_file.touch()

        records = load_students(filepath=self.test_file)
        self.assertEqual(records, [])

    def test_handle_non_list_root(self):
        """Test that a JSON file containing an object instead of list returns an empty list."""
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump({"single_record": "not_a_list"}, f)

        records = load_students(filepath=self.test_file)
        self.assertEqual(records, [])

    def test_search_students(self):
        """Test searching records by name or skill."""
        sample_students = [
            {"name": "Alice Smith", "age": 20, "skills": ["Python", "Django"], "cgpa": 8.5},
            {"name": "Bob Jones", "age": 22, "skills": ["Java", "Spring"], "cgpa": 7.9},
            {"name": "Charlie Pythonista", "age": 24, "skills": ["C#", ".NET"], "cgpa": 8.1}
        ]
        save_students(sample_students, filepath=self.test_file)

        # Search by skill "Python"
        skill_matches = search_students("python", filepath=self.test_file)
        # Should match Alice (skill Python) and Charlie (name Pythonista)
        self.assertEqual(len(skill_matches), 2)

        # Search by name "Bob"
        name_matches = search_students("bob", filepath=self.test_file)
        self.assertEqual(len(name_matches), 1)
        self.assertEqual(name_matches[0]["name"], "Bob Jones")

    def test_format_student(self):
        """Test formatting student display string."""
        record = {"name": "Reddiah", "age": 23, "skills": ["Python", "SQL"], "cgpa": 8.26}
        formatted = format_student(record)
        self.assertIn("Reddiah", formatted)
        self.assertIn("23", formatted)
        self.assertIn("8.26", formatted)
        self.assertIn("Python, SQL", formatted)


if __name__ == "__main__":
    unittest.main()
