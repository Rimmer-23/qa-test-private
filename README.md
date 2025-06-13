# QA Automation Test Task

Hi there! I’m sharing my QA Automation project built with Python, SQLite, and pytest. This project shows how I:

- **Create** an SQLite database with tables for ships, weapons, hulls, and engines  
- **Populate** it with random test data  
- **Generate** a randomized copy of that database via a pytest fixture  
- **Validate** all changes with 600 automated tests (3 checks per ship)

---

## What It Does

1. **db_creator.py**  
   - Builds `database/original.db`  
   - Defines tables: `weapons`, `hulls`, `engines`, `ships`  
   - Fills each table with random values (IDs like `Weapon-1…Weapon-20`, numeric attributes 1–20)

2. **conftest.py**  
   - Provides a session-scoped fixture that copies the original database  
   - For every ship, either swaps one component (weapon/hull/engine) or mutates a random parameter in each component  
   - Returns paths to both the original and randomized databases

3. **test_ships.py**  
   - Loads data from both databases  
   - Uses `pytest_generate_tests` to parameterize 600 test cases (200 ships × 3 components)  
   - Fails whenever it detects a swapped component or a changed numeric value, showing “before” and “after” details

---

## Usage

```bash
# 1. Clone this repo
git clone https://github.com/yourusername/qa_test_task.git
cd qa_test_task

# 2. (Optional) Create & activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install pytest
pip install pytest

# 4. Generate and populate the original database
python db_creator.py

# 5. Run all tests
python -m pytest -v test_ships.py

# 6. (Optional) Stop after first 10 failures
pytest -v --maxfail=10
