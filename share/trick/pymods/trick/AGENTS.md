# Python Modules Agent

Guidelines for Python code under `share/trick/pymods/trick`.

## Scope
This directory contains Python helpers and tests for Trick.

### Key Files
```
utils.py           - helper utilities
variable_server.py - variable server client
run_tests.py       - script to run pytest
tests/             - pytest based tests
```

## Style Guidelines
- Follow [PEP8](https://peps.python.org/pep-0008/).
- Use 4 spaces per indentation level.
- Include module level docstrings and descriptive comments.
- Prefer explicit is better than implicit.

### Template
```python
"""Short module description."""

class Example:
    def __init__(self):
        pass

def main():
    pass

if __name__ == "__main__":
    main()
```

## Common Actions
- Install dependencies: `pip install -r requirements.txt`.
- Run tests with `python run_tests.py`.

## Verification Questions
1. Does the code comply with PEP8 (indentation, naming)?
2. Are new features covered by tests in `tests/`?
3. Was `python run_tests.py` executed before committing?
4. Are docstrings provided for public classes and functions?
5. Are imports sorted and unused imports removed?
