# Lab 5 - Static Code Analysis Reflection

## 1. What did you learn from static code analysis?

Static code analysis helps identify potential security vulnerabilities, programming errors, and code-quality issues without requiring the program to be executed. In this lab, Pylint was used to evaluate code quality, Bandit to identify potential security issues, and Flake8 to check coding-style violations. Using these tools together provided a more comprehensive review of the attendance tracker.

## 2. What types of issues were identified in the original code?

The original attendance tracker contained security, functional, reliability, data-integrity, and maintainability issues. Examples included disabled TLS certificate verification, shell-based command execution, a mutable default argument, division by zero for empty attendance records, incorrect handling of the 75% attendance threshold, duplicate attendance entries, and inconsistent date formats. These issues demonstrated how seemingly small implementation choices can affect application security and correctness.

## 3. How were the identified issues resolved?

The code was revised to use safer HTTP request settings, obtain the API key from an environment variable, replace shell-based archive creation with Python's `tarfile` module, and use a default TLS context. Functional corrections included handling empty attendance records, using `>=` for the eligibility threshold, validating and normalizing dates, and preventing duplicate attendance entries. CSV export was also improved to reduce formula-injection risks, and the code was reformatted for readability and maintainability.

## 4. What did you learn from using multiple static analysis tools?

The lab demonstrated that different tools focus on different aspects of code quality. Pylint evaluates code quality and maintainability, Bandit checks for common security issues, and Flake8 identifies style and formatting violations. No single tool guarantees that a program is completely correct or secure, so tool results should be considered alongside functional testing and manual review.

## Final Outcome

After correction, the attendance tracker executed successfully. The final verification reported a Pylint score of 10.00/10, no issues identified by Bandit, and no violations reported by Flake8. This exercise reinforced the importance of iterative code review, secure programming practices, and validating changes after fixing identified issues.

