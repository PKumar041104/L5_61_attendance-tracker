# Lab 5: Static Code Analysis — Student Attendance Tracker
## NAME: PRATHAM KUMAR
## SRN No.: PES2UG24CS368
## SECTION: F
**Your file:** `attendance_tracker.py`
**Python:** 3.10 or newer

Follow the lab handout for the full instructions.

## About the program

A college attendance tracker. It marks daily attendance per student, works out attendance percentages, applies the 75% exam-eligibility rule, lists students with a shortage, exports a CSV, schedules reminders and can sync to an ERP system and back up reports.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Install the tools:**
   ```bash
   python -m pip install pylint bandit flake8 requests
   ```
   `requests` is installed as well because the program imports it; without it the program stops with `ModuleNotFoundError`.

2. **Run it first** and read the output carefully:
   ```bash
   python attendance_tracker.py
   ```
   It runs a short built-in demo and prints the results; it does not ask for input. Read every line and ask whether a sensible program would print that. Not every problem in this file is something a tool will flag, so pay attention to output that looks wrong.



3. **Run the analysis** and save the reports:
   ```bash
   python -m pylint attendance_tracker.py > pylint_report.txt
   python -m bandit -r attendance_tracker.py > bandit_report.txt
   python -m flake8 attendance_tracker.py > flake8_report.txt
   ```
   Use the `python -m` form: it works everywhere, including Windows where a bare `pylint` is often "not recognized". The tools exit with a non-zero status whenever they find issues; that is expected, not an error. In Windows PowerShell 5.1, `>` saves files as UTF-16; if a report looks garbled, use `python -m pylint attendance_tracker.py | Out-File -Encoding utf8 pylint_report.txt` instead.

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ... | ... | ... | ... | ... |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

1. `attendance_tracker.py`: your cleaned version, with at least 4 issues fixed.
2. `issues.md`: the completed issue table.
3. `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.

## Static Code Analysis Results

This section documents the static code analysis performed for Lab 5 on
the Attendance Tracker program. The source code was reviewed and updated
using **Pylint**, **Bandit**, and **Flake8**. Issues identified during
the initial analysis were documented in `issues.md`, and the relevant
corrections were applied to `attendance_tracker.py`.

### Tools Used

  -----------------------------------------------------------------------
  Tool                    Purpose                 Final result
  ----------------------- ----------------------- -----------------------
  Pylint                  Checks Python code      **10.00/10**
                          quality, common         
                          programming errors, and 
                          maintainability         

  Bandit                  Checks Python code for  **No issues
                          common security issues  identified**

  Flake8                  Checks Python style and **No violations
                          PEP 8-related           reported**
                          violations              
  -----------------------------------------------------------------------

The final reports are saved in the `evidence/` directory. The
`*_before.txt` files preserve the initial analysis results, while the
`*_after.txt` files record the final checks after the fixes.
`flake8_after.txt` is empty because Flake8 produced no violations in the
final run.

### Summary of Corrections

The review covered security, functional correctness, and
maintainability. Corrections included:

-   Restoring TLS certificate verification and replacing insecure TLS
    configuration with a secure default context.
-   Reading the API key from an environment variable rather than
    hard-coding it.
-   Replacing shell-based archive creation with Python's `tarfile` API.
-   Adding HTTP timeout and response-status handling.
-   Correcting mutable default arguments and handling zero-record
    calculations safely.
-   Preventing duplicate attendance entries and validating date input.
-   Mitigating CSV formula injection during export.
-   Improving resource handling, encoding, naming, documentation, and
    code style.

The issue descriptions, classifications, relevant line references, and
fix approaches are documented in `issues.md`. The learning and
reflection responses are documented in `reflection.md`.

### Repository Structure and Evidence

The repository is organized as follows:

``` text
L5_61_attendance-tracker/
├── attendance_tracker.py
├── issues.md
├── reflection.md
├── README.md
├── .gitignore
└── evidence/
    ├── Figure_01_Fresh_Repository_Clone.png
    ├── Figure_2_Baseline_Execution_of_the_Original_Attendance_Tracker.png
    ├── Figure_3_Initial_Pylint_Analysis_of_the_Original_Attendance_Tracker.png
    ├── Figure_4_Initial_Bandit_Security_Analysis_of_the_Attendance_Tracker.png
    ├── Figure_5_Initial_Flake8_Analysis_of_the_Original_Attendance_Tracker.png
    ├── Figure_6_Final_Verification_of_the_Corrected_Attendance_Tracker_Using_Pylint_Bandit_and_Flake8.png
    ├── pylint_before.txt
    ├── bandit_before.txt
    ├── flake8_before.txt
    ├── pylint_after.txt
    ├── bandit_after.txt
    └── flake8_after.txt
```

**Evidence guide**

  ------------------------------------------------------------------------------------------------------------------------------------------
  Evidence                                                                                               What it supports
  ------------------------------------------------------------------------------------------------------ -----------------------------------
  `Figure_01_Fresh_Repository_Clone.png`                                                                 Shows the repository cloned locally
                                                                                                         before the work.

  `Figure_2_Baseline_Execution_of_the_Original_Attendance_Tracker.png`                                   Shows execution of the original
                                                                                                         program before applying
                                                                                                         corrections.

  `Figure_3_Initial_Pylint_Analysis_of_the_Original_Attendance_Tracker.png`                              Shows the initial Pylint analysis.

  `Figure_4_Initial_Bandit_Security_Analysis_of_the_Attendance_Tracker.png`                              Shows the initial Bandit security
                                                                                                         analysis.

  `Figure_5_Initial_Flake8_Analysis_of_the_Original_Attendance_Tracker.png`                              Shows the initial Flake8 analysis.

  `Figure_6_Final_Verification_of_the_Corrected_Attendance_Tracker_Using_Pylint_Bandit_and_Flake8.png`   Shows final verification using the
                                                                                                         three analysis tools.

  `pylint_before.txt`, `bandit_before.txt`, `flake8_before.txt`                                          Text reports from the initial
                                                                                                         analysis.

  `pylint_after.txt`, `bandit_after.txt`, `flake8_after.txt`                                             Text reports from the final
                                                                                                         analysis after corrections.
  ------------------------------------------------------------------------------------------------------------------------------------------

### How to Run the Program

Run the program from the repository root using Python:

``` bash
python attendance_tracker.py
```

The program demonstrates attendance calculations, shortage checking,
date-based register entries, CSV export, and a demonstration reminder
job. The ERP synchronization step is intentionally skipped in the
offline demonstration.

### Re-run Static Analysis

Install the tools if they are not already installed:

``` bash
python -m pip install pylint bandit flake8
```

Run each tool from the repository root:

``` bash
python -m pylint attendance_tracker.py
python -m bandit -r attendance_tracker.py
python -m flake8 attendance_tracker.py
```

To preserve fresh reports, redirect each command's output to the
corresponding files in `evidence/`. For example, in Windows Command
Prompt:

``` bat
python -m pylint attendance_tracker.py > evidence\pylint_after.txt 2>&1
python -m bandit -r attendance_tracker.py > evidence\bandit_after.txt 2>&1
python -m flake8 attendance_tracker.py > evidence\flake8_after.txt 2>&1
```

**Note:** The results above describe the final checks recorded for this
submission. If the code changes, rerun all three tools and update the
evidence reports so they match the submitted version.
