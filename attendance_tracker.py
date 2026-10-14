"""Attendance tracker with validated records and safer utilities."""

import csv
import os
import ssl
import tarfile
from datetime import date
from pathlib import Path

import requests

students = {}
ERP_URL = "https://erp.college.example/api/attendance"
MIN_ATTENDANCE = 75
VALID_STATUSES = {"P", "A", "L", "H"}


def add_student(roll_no, name, section="A"):
    """Add a student's basic details and initialize attendance records."""
    if not roll_no.strip() or not name.strip():
        raise ValueError("Roll number and name cannot be empty.")
    students[roll_no] = {"name": name, "section": section, "records": []}


def mark_attendance(roll_no, attendance_date, status, register=None):
    """Record attendance once per student and date."""
    if roll_no not in students:
        raise KeyError(f"Unknown student roll number: {roll_no}")

    try:
        normalized_date = date.fromisoformat(attendance_date).isoformat()
    except (TypeError, ValueError) as exc:
        raise ValueError("Date must use YYYY-MM-DD format.") from exc

    normalized_status = status.strip().upper()
    if normalized_status not in VALID_STATUSES:
        raise ValueError("Status must be P, A, L, or H.")

    if any(
        item[0] == normalized_date
        for item in students[roll_no]["records"]
    ):
        raise ValueError(
            f"Duplicate attendance for {roll_no} on {normalized_date}."
        )

    if register is None:
        register = {}

    entries = register.setdefault(normalized_date, [])
    if roll_no not in entries:
        entries.append(roll_no)

    students[roll_no]["records"].append(
        (normalized_date, normalized_status)
    )
    return register


def attendance_percentage(roll_no):
    """Return the percentage of recorded sessions marked present."""
    records = students[roll_no]["records"]
    if not records:
        return 0

    present = sum(status == "P" for _, status in records)
    return int(present / len(records) * 100)


def is_eligible(percentage):
    """Return whether attendance meets the inclusive minimum."""
    return percentage >= MIN_ATTENDANCE


def shortage_list():
    """Return students below the attendance threshold."""
    return [
        roll_no
        for roll_no in students
        if not is_eligible(attendance_percentage(roll_no))
    ]


def has_long_absence(roll_no, days=3):
    """Check for a consecutive run of absent attendance records."""
    statuses = [status for _, status in students[roll_no]["records"]]
    return any(
        statuses[index:index + days] == ["A"] * days
        for index in range(max(0, len(statuses) - days + 1))
    )


def latest_date(roll_no):
    """Return the latest recorded date in ISO format, or None."""
    records = students[roll_no]["records"]
    if not records:
        return None

    latest = max(date.fromisoformat(item[0]) for item in records)
    return latest.isoformat()


def _spreadsheet_safe(value):
    """Protect spreadsheet exports from formula-leading text values."""
    text_value = str(value)
    if text_value.startswith(("=", "+", "-", "@", "\t", "\r")):
        return "'" + text_value
    return text_value


def export_csv(path="attendance.csv"):
    """Export attendance percentages to a UTF-8 CSV file."""
    output_path = Path(path)

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["roll_no", "name", "percentage"])

        for roll_no, details in students.items():
            writer.writerow([
                _spreadsheet_safe(roll_no),
                _spreadsheet_safe(details["name"]),
                attendance_percentage(roll_no),
            ])

    return str(output_path)


def sync_to_erp(roll_no):
    """Send attendance to the ERP with verified TLS and a timeout."""
    api_key = os.getenv("ERP_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Set ERP_API_KEY before ERP synchronization."
        )

    response = requests.post(
        ERP_URL,
        json={
            "roll_no": roll_no,
            "pct": attendance_percentage(roll_no),
        },
        headers={"X-API-Key": api_key},
        timeout=10,
    )
    response.raise_for_status()
    return response.status_code


def backup_reports():
    """Archive CSV reports without invoking a shell."""
    backup_path = Path("reports_backup.tgz")

    with tarfile.open(backup_path, "w:gz") as archive:
        for csv_path in sorted(Path.cwd().glob("*.csv")):
            if csv_path.is_file():
                archive.add(csv_path, arcname=csv_path.name)

    return str(backup_path)


def legacy_channel():
    """Create a TLS context using secure platform defaults."""
    return ssl.create_default_context()


def run_job(command, shell=False):
    """Describe a job configuration without executing it."""
    return {"command": command, "shell": shell}


def schedule_reminders():
    """Return a reminder job as an argument list, not a shell string."""
    return run_job(["send_sms", "--shortage"])


def main():
    """Run the built-in offline attendance demonstration."""
    students.clear()
    add_student("R01", "Aditi")
    add_student("R02", '=HYPERLINK("http://evil.example","Bharat")')

    register = {}

    for attendance_date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "P"),
        ("2026-09-03", "L"),
        ("2026-09-04", "P"),
        ("2026-09-05", "H"),
    ]:
        mark_attendance(
            "R01", attendance_date, status, register
        )

    for attendance_date, status in [
        ("2026-09-01", "P"),
        ("2026-09-02", "A"),
        ("2026-09-03", "A"),
        ("2026-09-04", "A"),
        ("2026-09-05", "P"),
    ]:
        mark_attendance(
            "R02", attendance_date, status, register
        )

    print("R01 attendance %:", attendance_percentage("R01"))
    print("R02 attendance %:", attendance_percentage("R02"))
    print("Is 75% eligible?", is_eligible(75))
    print("Shortage list:", shortage_list())
    print("R02 long absence?", has_long_absence("R02"))
    print("R02 latest date:", latest_date("R02"))
    print(
        "Register entries for 2026-09-01:",
        register["2026-09-01"],
    )
    print("Exported to:", export_csv())
    print("Reminder job:", schedule_reminders())
    print("ERP sync skipped (demo runs offline)")


if __name__ == "__main__":
    main()
