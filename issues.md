# Lab 5: Static Code Analysis
## Warehouse Stock Manager — Issues Report

### Objective

To identify and resolve code quality, security, maintainability,
and logical issues using Pylint, Bandit, and Flake8.

The original program was analyzed before making changes.
The findings below describe the original source code.

## Issues Identified

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe use of eval() | Security | 62, 80 | eval() can execute arbitrary Python expressions and introduce security vulnerabilities. | Replaced dynamic evaluation with a restricted AST-based arithmetic evaluator and a normal print statement. |
| Hardcoded supervisor password | Security | 10 | The supervisor password was stored directly in the source code. | Moved password configuration to the WAREHOUSE_SUPERVISOR_PASSWORD environment variable. |
| Weak MD5 hashing | Security | 31 | MD5 was used to generate SKU fingerprints. | Replaced MD5 with SHA-256 for the printed SKU fingerprint. |
| Mutable default argument | Bug | 12 | history=[] could cause a list to be shared between function calls. | Changed the default to None and initialized a new list when required. |
| Bare except clause | Reliability | 23-24 | The program silently ignored every exception, making unexpected errors difficult to identify. | Removed the bare exception handler and validated inputs explicitly. |
| Negative stock quantities | Logical bug | 12, 19-24 | Negative quantities could result in invalid inventory levels. | Added quantity validation and prevented stock removal beyond the available quantity. |
| Invalid SKU types | Input validation | 14, 71 | The original demonstration accepted an integer SKU instead of a non-empty string. | Added SKU validation and used a string SKU in the demonstration. |
| Unsafe file handling | Code quality | 34, 40, 63 | Files were opened without explicit encoding and were not consistently managed with context managers. | Used with open() and encoding="utf-8". |
| Unused variable | Code quality | 54 | total_units was calculated but never used. | Removed the unused variable. |
| Missing docstrings | Maintainability | Multiple | The original module and functions lacked documentation. | Added module and function docstrings. |
| Incorrect function naming | Style | Multiple | Function names such as addStock and getStock did not follow Python naming conventions. | Renamed functions using snake_case. |
| Unused imports | Style | 2, 4 | The logging and os imports were reported as unused in the original program. | Removed logging and used os for environment-based password configuration. |
| Missing file encoding | Code quality | 34, 40, 63 | File operations relied on the platform's default encoding. | Specified UTF-8 encoding for file operations. |
| Formatting violations | Style | Multiple | Long lines, trailing whitespace, and missing final newline violated formatting rules. | Reformatted the source and verified it using Flake8. |
| Insufficient JSON validation | Reliability | 34-35 | Loaded JSON data was accepted without validating the structure and stock entries. | Added validation for the loaded dictionary, SKU keys, and quantities. |

## Tools Used

### Pylint
Used to identify programming issues, naming violations,
missing documentation, unused variables, and code quality problems.

### Bandit
Used to identify potentially insecure coding patterns,
including unsafe dynamic evaluation and weak hashing.

### Flake8
Used to identify formatting problems, unused imports,
line-length violations, and other style issues.

## Results

The original Pylint score was 4.48/10.

After the code improvements, Pylint reported a score of 9.84/10.

Bandit initially reported five findings, including two uses of eval(),
a hardcoded password, a bare exception handler, and MD5 hashing.

After the changes, Bandit reported no security issues.

Flake8 initially reported multiple formatting violations.
The source was subsequently corrected and checked again.

The final results should be confirmed using the latest reports
generated after the final source-code changes.