# Student Data Management System

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-pep8-green.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Tests: Passing](https://img.shields.io/badge/tests-passing-brightgreen.svg)]()

A robust, modular, and fault-tolerant Python application for managing student records. It stores structured student records in JSON format and implements comprehensive data validation, modular architecture, and resilient error recovery mechanisms.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture & Design](#architecture--design)
- [Project Structure](#project-structure)
- [Data Schema](#data-schema)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage Guide](#usage-guide)
  - [Interactive Menu Options](#interactive-menu-options)
- [Automated Testing](#automated-testing)
- [Error Handling & Fault Tolerance](#error-handling--fault-tolerance)
- [Roadmap](#roadmap)
- [Author](#author)
- [License](#license)

---

## Overview

The **Student Data Management System** provides a lightweight yet production-grade Command-Line Interface (CLI) backed by a separate data access module (`student_manager.py`). The application enables users to add, view, and search student records while ensuring persistence in a JSON database (`students.json`).

Designed with clean architecture principles:
- **Zero Third-Party Dependencies**: Relies purely on the Python Standard Library (`json`, `pathlib`, `typing`, `unittest`).
- **Separation of Concerns**: User interaction is isolated to `main.py`, while data operations and validation reside in `student_manager.py`.
- **Fault-Tolerant File I/O**: Gracefully detects and handles missing files, malformed JSON, and unexpected data structures without crashing.

---

## Key Features

- **Interactive Data Entry**: Prompts users for student details with strict validation rules (non-empty strings, bounded integers, formatted floats).
- **In-Memory Dictionary Representation**: Records are modeled as native Python dictionaries before serialization.
- **Persistent JSON Storage**: Records are automatically formatted and saved with standard 4-space indentation for human readability.
- **Append & Read Workflows**: Reads existing datasets seamlessly and appends new entries without data loss.
- **Fault Tolerance**:
  - Missing file? Automatically initializes an empty dataset.
  - Corrupt or malformed JSON? Logs a clear diagnostic warning and returns an empty list safely.
  - Non-list JSON root? Validates schema integrity.
- **Search Capabilities**: Query records in real time by student name or matching skill set.
- **Unit Tested**: Fully tested against 9 automated test scenarios with 100% pass rate.

---

## Architecture & Design

```
+-------------------------------------------------------------+
|                           main.py                           |
|       (CLI Interface, Input Validation & User Prompts)      |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                      student_manager.py                     |
|  - create_student_record()      - load_students()           |
|  - save_students()              - append_student()          |
|  - search_students()            - format_student()          |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                        students.json                        |
|              (Persistent Structured Data Store)             |
+-------------------------------------------------------------+
```

---

## Project Structure

```text
Student Data Management System/
│
├── main.py                 # CLI interface and interactive menu loop
├── student_manager.py      # Core business logic and file management module
├── students.json           # JSON database storing student records
├── test_student_manager.py # Automated test suite (9 test cases)
├── requirements.txt        # Dependency specification (Standard Library only)
├── .gitignore              # Standard Python ignores (__pycache__, venv, etc.)
└── README.md               # Project documentation
```

---

## Data Schema

Each student record is stored in a structured JSON list:

```json
[
    {
        "name": "Reddiah",
        "age": 23,
        "skills": [
            "Python",
            "SQL",
            "AI"
        ],
        "cgpa": 8.26
    }
]
```

### Field Definitions

| Field | Type | Description | Constraints |
| :--- | :--- | :--- | :--- |
| `name` | `string` | Full name of the student | Must not be blank |
| `age` | `integer` | Age in years | Between `1` and `120` |
| `skills` | `list[string]` | Acquired skills / technologies | At least 1 non-empty skill |
| `cgpa` | `float` | Cumulative Grade Point Average | Between `0.00` and `10.00` |

---

## Getting Started

### Prerequisites

- **Python**: Version `3.8` or higher
- **Git** (optional, for version control)

Check your installed version:
```bash
python --version
```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Reddiah16/Student-Data-Management-System.git
   cd "Student Data Management System"
   ```

2. **Dependencies**:
   This project uses only built-in modules. No `pip install` commands are required!
   ```bash
   # Optional: review requirements
   cat requirements.txt
   ```

---

## Usage Guide

Run the main application from your terminal:

```bash
python main.py
```

### Interactive Menu Options

```text
=============================================
     STUDENT DATA MANAGEMENT SYSTEM
=============================================
 [1] Add New Student Record
 [2] View All Student Records
 [3] Search Student (by Name / Skill)
 [4] Exit
=============================================
Enter your choice (1-4):
```

#### 1. Adding a Student
- Prompts for Name, Age, Skills (comma-separated, e.g., `Python, React, Docker`), and CGPA.
- Creates the dictionary and appends it to `students.json`.

#### 2. Viewing Records
- Neatly tabularizes all existing student records with formatted indices and statistics.

#### 3. Searching
- Allows keyword search matching either student names or specific skills (case-insensitive).

#### 4. Safe Exit
- Exits cleanly with exit status `0`. Supports `Ctrl+C` interrupt handling without messy tracebacks.

---

## Automated Testing

A comprehensive unit test suite is included to guarantee correctness across all module operations:

```bash
python test_student_manager.py
```
*(or via the unittest module)*
```bash
python -m unittest test_student_manager.py
```

### Test Coverage Highlights

- [x] Dictionary creation and data normalization
- [x] Multi-record save and load roundtripping
- [x] Record appending to existing datasets
- [x] Missing file tolerance (`FileNotFoundError` handling)
- [x] Corrupted / invalid JSON handling (`json.JSONDecodeError`)
- [x] Empty file detection
- [x] Non-list JSON root validation
- [x] Name and skill query matching
- [x] String display formatting

---

## Error Handling & Fault Tolerance

| Scenario | Handled Condition | Behavior |
| :--- | :--- | :--- |
| **File Not Found** | `FileNotFoundError` | Notifies user and initializes an empty in-memory list without crashing. |
| **Corrupt JSON Syntax** | `json.JSONDecodeError` | Emits a warning explaining the parsing failure and safely returns `[]`. |
| **Empty File** | `len(content) == 0` | Safely handles 0-byte files without syntax error exceptions. |
| **Invalid Schema** | `not isinstance(data, list)` | Detects non-list structures and protects against downstream TypeError crashes. |
| **Keyboard Interrupt** | `KeyboardInterrupt`, `EOFError` | Catches `Ctrl+C` / `Ctrl+D` and cleanly exits the application. |

---

## Roadmap

- [ ] Export records to CSV and Excel formats
- [ ] Update / Edit existing student records
- [ ] Delete student records by ID/Name
- [ ] Web dashboard using Streamlit or FastAPI

---

## Author

**Reddiah**  
- GitHub: [@Reddiah16](https://github.com/Reddiah16)  
- Email: [reddiah151@gmail.com](mailto:reddiah151@gmail.com)

---

## License

This project is licensed under the [MIT License](LICENSE).
