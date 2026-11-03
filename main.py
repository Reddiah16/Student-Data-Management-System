"""
main.py
=======
CLI entry point for the Student Data Management System.
Allows users to:
1. Accept student details via prompt.
2. Store them in a dictionary.
3. Save and append to a JSON file.
4. View existing records from the JSON file.
5. Search records.
6. Handle errors cleanly.
"""

import sys
from pathlib import Path

# Ensure the module directory is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from student_manager import (
    create_student_record,
    load_students,
    append_student,
    search_students,
    format_student,
    DEFAULT_FILE_PATH,
)


def get_non_empty_input(prompt: str) -> str:
    """Prompts until a non-empty string is provided."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  [!] Input cannot be empty. Please try again.")


def get_valid_integer(prompt: str, min_val: int = 1, max_val: int = 120) -> int:
    """Prompts until a valid integer within the range is provided."""
    while True:
        val_str = input(prompt).strip()
        try:
            val = int(val_str)
            if min_val <= val <= max_val:
                return val
            print(f"  [!] Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  [!] Invalid number. Please enter a valid integer.")


def get_valid_float(prompt: str, min_val: float = 0.0, max_val: float = 10.0) -> float:
    """Prompts until a valid float within the range is provided."""
    while True:
        val_str = input(prompt).strip()
        try:
            val = float(val_str)
            if min_val <= val <= max_val:
                return round(val, 2)
            print(f"  [!] Please enter a CGPA between {min_val:.1f} and {max_val:.1f}.")
        except ValueError:
            print("  [!] Invalid input. Please enter a numeric value (e.g. 8.26).")


def get_skills_input(prompt: str) -> list[str]:
    """Prompts user for comma-separated skills."""
    while True:
        raw_skills = input(prompt).strip()
        if not raw_skills:
            print("  [!] Please enter at least one skill (e.g., Python, SQL).")
            continue
        skills = [s.strip() for s in raw_skills.split(",") if s.strip()]
        if skills:
            return skills
        print("  [!] Please enter valid skill names.")


def handle_add_student():
    """Collects student details, creates dictionary, and appends to JSON."""
    print("\n" + "=" * 45)
    print("             ADD NEW STUDENT")
    print("=" * 45)

    name = get_non_empty_input("Enter Student Name: ")
    age = get_valid_integer("Enter Age (1-120): ")
    skills = get_skills_input("Enter Skills (separated by commas, e.g., Python, SQL, AI): ")
    cgpa = get_valid_float("Enter CGPA (0.0 - 10.0): ")

    # Store information in a Python dictionary
    student_dict = create_student_record(name=name, age=age, skills=skills, cgpa=cgpa)

    print("\nCreated Student Dictionary:")
    print(student_dict)

    # Save student record by appending to JSON file
    success = append_student(student_dict)
    if success:
        print(f"\n[+] Student '{name}' successfully saved to {DEFAULT_FILE_PATH.name}!")
    else:
        print("\n[-] Failed to save student record.")


def handle_view_students():
    """Reads and displays all student records from the JSON file."""
    print("\n" + "=" * 70)
    print("                      ALL STUDENT RECORDS")
    print("=" * 70)

    students = load_students()

    if not students:
        print("No student records found.")
        return

    print(f"Total students: {len(students)}\n")
    print("-" * 70)
    for idx, student in enumerate(students, 1):
        print(f"[{idx}] {format_student(student)}")
    print("-" * 70)


def handle_search_students():
    """Searches for students by name or skill."""
    print("\n" + "=" * 45)
    print("               SEARCH STUDENTS")
    print("=" * 45)

    query = get_non_empty_input("Enter name or skill to search: ")
    results = search_students(query)

    if not results:
        print(f"\nNo students found matching '{query}'.")
        return

    print(f"\nFound {len(results)} matching record(s):")
    print("-" * 70)
    for idx, student in enumerate(results, 1):
        print(f"[{idx}] {format_student(student)}")
    print("-" * 70)


def display_menu():
    """Displays main navigation menu."""
    print("\n" + "=" * 45)
    print("     STUDENT DATA MANAGEMENT SYSTEM")
    print("=" * 45)
    print(" [1] Add New Student Record")
    print(" [2] View All Student Records")
    print(" [3] Search Student (by Name / Skill)")
    print(" [4] Exit")
    print("=" * 45)


def main():
    """Main program execution loop."""
    print("Welcome to Student Data Management System!")
    print(f"Active database: {DEFAULT_FILE_PATH.name}")

    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                handle_add_student()
            elif choice == "2":
                handle_view_students()
            elif choice == "3":
                handle_search_students()
            elif choice == "4":
                print("\nThank you for using Student Data Management System. Goodbye!\n")
                sys.exit(0)
            else:
                print("  [!] Invalid choice. Please choose an option from 1 to 4.")

        except (KeyboardInterrupt, EOFError):
            print("\n\nOperation cancelled by user. Exiting...")
            sys.exit(0)


if __name__ == "__main__":
    main()
