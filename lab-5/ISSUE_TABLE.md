# Lab 5: Static Code Analysis

## Identified issues and fixes

| Issue | Type | Original location | Description | Fix approach |
|---|---|---:|---|---|
| Mutable default argument | Bug | `createAccount`, line 12 | `transactions=[]` is shared between calls. | Use `None` as the default and create a new list inside the function. |
| Bare exception handler | Bug / maintainability | `deposit`, lines 20-23 | A bare `except` hides every failure, including programming errors. | Validate the account and amount, then return a success/failure result. |
| Unsafe `eval()` | Security | `compute_bonus`, line 34 | Arbitrary Python expressions can execute code. | Parse the expression with `ast` and allow only arithmetic on `bal` and numeric constants. |
| Weak MD5 password/PIN hash | Security | `get_hash`, line 39 | MD5 is unsuitable for password/PIN storage. | Use salted PBKDF2-HMAC-SHA256 and constant-time verification. |
| Non-cryptographic random PIN | Security | `generate_temp_pin`, line 43 | `random` is not designed for security-sensitive tokens. | Use `secrets.randbelow`. |
| Unclosed file handling | Reliability | `backup_data`, lines 47-49 | Manual open/close may leave the file open if writing fails. | Use a context manager and specify UTF-8 encoding. |
| Shell command construction | Security | `backup_data`, line 50 | Passing a filename to `os.system` can allow shell injection. | Remove the shell call and print a fixed completion message in `main`. |
| Hard-coded secret | Security | `main`, line 54 | A fixed admin token is exposed in source control and printed. | Remove the unused token and its output. |
| Unused import / variable | Maintainability | Imports and `withdraw`, lines 6 and 27 | `sys` and `service_fee` are unused. | Remove them. |
| Missing executable guard | Maintainability | End of file | Importing the module runs the demonstration automatically. | Call `main()` only under `if __name__ == "__main__":`. |
| Inconsistent naming and formatting | Style | Multiple lines | `createAccount` and percent-formatting do not follow common Python conventions. | Rename to `create_account`, use f-strings, and apply consistent formatting. |

## Reflection

Static code analysis helps find problems before a program is deployed. Pylint focuses on code quality and likely programming mistakes, Flake8 checks style and formatting, and Bandit highlights common security risks. In this program, the most important issue was the use of `eval()`, because it could execute arbitrary input. The mutable default argument and broad exception handler could also make the program behave unpredictably. Fixing these issues made the code safer, easier to read, and easier to maintain.

A limitation of static analysis is that tools report patterns and possible risks, not the full intent of a program. Findings still need to be reviewed, and changes should be tested to ensure that the program's expected behaviour is preserved.
