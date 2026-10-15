# Lab 5: Static Code Analysis
## Reflection — Warehouse Stock Manager

### 1. What is static code analysis, and why is it useful?

Static code analysis is the process of examining source code without
executing the program to identify potential bugs, security
vulnerabilities, and coding standard violations.

It is useful because it helps developers detect problems early,
improve maintainability, and reduce the risk of defects reaching
production. It also encourages consistent coding practices.

### 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint focuses on overall code quality, programming practices,
naming conventions, missing documentation, unused variables,
and potential logical errors.

Bandit focuses on security-related coding patterns and identifies
potential vulnerabilities, such as unsafe dynamic execution,
hardcoded credentials, and weak cryptographic practices.

Flake8 focuses on Python style and formatting. It detects problems
such as unused imports, incorrect whitespace, long lines,
and violations of PEP 8 conventions.

Using all three tools provides complementary checks for code
quality, security, and consistency.

### 3. What problems were identified and how were they fixed?

The original warehouse stock manager contained several problems.

The use of eval() created a security risk because it could execute
arbitrary Python expressions. It was replaced with a restricted
AST-based arithmetic evaluator.

The supervisor password was hardcoded in the source code.
It was moved to an environment variable.

MD5 was replaced with SHA-256 for generating SKU fingerprints.

The mutable default argument history=[] was changed to history=None
so that a list could be initialized when required.

The bare except clause was removed, and explicit validation was
introduced for SKUs and stock quantities.

File operations were updated to use context managers and explicit
UTF-8 encoding. Missing documentation, naming violations,
unused variables, and formatting issues were also addressed.

### 4. What did you learn from this lab?

This lab demonstrated that a program can execute successfully
while still containing security vulnerabilities, logical bugs,
and maintainability problems.

Pylint, Bandit, and Flake8 identify different categories of issues.
Using multiple tools provides a more comprehensive assessment
than relying on a single tool.

I also learned that static analysis findings need to be reviewed
and understood before making changes. Fixes must preserve the
intended functionality and should be verified by rerunning the
program and the analysis tools.

The original Pylint score was 4.48/10. After the improvements,
the score increased to 9.84/10. Bandit reported no issues in the
subsequent scan. The final Flake8 result should be verified using
the latest report.