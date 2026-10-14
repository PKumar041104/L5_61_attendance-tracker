# Lab 5 - Static Code Analysis Issues

The following table documents issues identified during the analysis of the original attendance tracker source code. Line numbers refer to the original source before correction and should be cross-checked against the saved baseline or original tool reports. Multiple findings may describe the same underlying cause.

| Issue | Type | Original line(s) | Description | Fix Approach |
|---|---|---|---|---|
| TLS certificate verification disabled | Security - High | Approx. 60; verify against baseline | Using `verify=False` disables server certificate verification and can expose HTTPS communication to interception. | Removed the override, retained default TLS certificate verification, added a request timeout, and checked the HTTP response status. |
| Shell command with wildcard | Security - High | Approx. 64; verify against baseline | Using `subprocess.Popen()` with `shell=True` and a wildcard can introduce command-injection and unsafe file-handling risks. | Replaced shell-based archive creation with Python's `tarfile` module and path handling. |
| Hard-coded API-key configuration | Security | Approx. 10, 60; verify against baseline | API credentials should not be embedded directly in source code. Verify whether the original value was an actual credential or a placeholder. | Read `ERP_API_KEY` from an environment variable. If a real credential was exposed, rotate it. |
| Outdated TLS protocol | Security - Medium | Approx. 66; verify against baseline | Explicitly selecting `ssl.PROTOCOL_TLSv1` uses an obsolete TLS protocol configuration. | Replaced it with `ssl.create_default_context()` to use secure system defaults. |
| Missing HTTP timeout | Reliability | Approx. 60; verify against baseline | An ERP request without a timeout may wait indefinitely if the server does not respond. | Added a 10-second timeout and `raise_for_status()` to detect unsuccessful HTTP responses. |
| Mutable default argument | Functional bug | Approx. 18; verify against baseline | Using `register={}` as a default argument can cause mutable state to be shared between function calls. | Changed the default to `None` and initialized a register for each call. |
| Attendance threshold boundary | Functional bug | Approx. 29; verify against baseline | Using `>` instead of `>=` incorrectly rejects a student whose attendance is exactly 75%. | Used `>=` so attendance at the configured threshold qualifies. |
| Division by zero | Functional bug | Approx. 23-26; verify against baseline | Calculating attendance percentage without checking for empty attendance records can cause division by zero. | Return 0% when no attendance records are available. |
| Duplicate attendance and inconsistent dates | Data integrity | Approx. 18, 38-39; verify against baseline | Duplicate entries can inflate attendance counts, while inconsistent date formats can cause incorrect date comparisons and sorting. | Validate and normalize dates to ISO format and reject duplicate student/date entries. |
| CSV formula injection | Security | Approx. 20, 52-56; verify against baseline | Text beginning with spreadsheet formula characters may be interpreted as a formula when a CSV file is opened in spreadsheet software. | Sanitize formula-leading text values before exporting them to CSV. |
| Unsafe file handling | Reliability / maintainability | Approx. 51-56; verify against baseline | CSV export without a context manager and explicit encoding can make resource management and consistent file output less reliable. | Used `Path.open()` with UTF-8 encoding and `newline=""` in a context manager. |
| Style and maintainability issues | Code quality | Multiple lines | Naming inconsistencies, missing docstrings, unused imports, and overly long lines reduce readability and maintainability. | Used consistent snake_case naming, docstrings, cleaned imports, and formatted long lines. |

## Final Verification

The corrected program was executed successfully. The final static analysis results were:

- **Pylint:** 10.00/10.
- **Bandit:** No issues identified; zero findings across all reported severity levels.
- **Flake8:** Completed without reporting violations.

The demonstration runs in offline mode and does not perform an actual ERP synchronization. ERP synchronization requires the appropriate `ERP_API_KEY` environment variable and a reachable ERP endpoint.

These results describe the final checks performed and do not imply that static analysis can detect every possible software defect or security vulnerability.