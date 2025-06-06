# Root AGENTS

This repository contains the **Trick Simulation Environment**.  Contributors should consult this file and any nested `AGENTS.md` files before making changes.

## Index of Agents
- `/AGENTS.md` (this file): repository wide guidelines.
- `/docs/AGENTS.md`: rules for documentation within `docs/`.
- `/trick_source/AGENTS.md`: rules for C/C++ source under `trick_source/`.
- `/share/trick/pymods/trick/AGENTS.md`: rules for Python modules under `share/trick/pymods/trick/`.

These nested files extend the instructions here.  When editing a file, follow the instructions for the most specific `AGENTS.md` in its path.

## General Style
- Use **four spaces** for indentation.
- Keep lines under **120 characters** when practical.
- Include a license header when creating new source files (see existing files for examples).
- Commit messages should follow the pattern:
  ```
  Short summary (50 chars or less)

  More detailed explanation of the change.
  ```

## Building and Testing
- After modifying C/C++ or Python code run `make test` from the repository root.  This builds the project and executes the test suite.
- Python modules in `share/trick/pymods/trick` contain additional tests that can be run with `python run_tests.py` from that directory.
- If the environment prevents the tests from running, note this in your pull request.
- Documentation only changes do not require running the full test suite but should be spell checked.

## Repository Overview
```
CMakeModules/    - CMake build helpers
CMakeTestFiles/  - Example CMake projects
autoconf/        - Autotools scripts
bin/             - command line utilities (Perl, shell)
docs/            - user and developer documentation
include/         - public header files
libexec/         - build and maintenance scripts
share/           - configuration files, python modules, templates
trick_source/    - core Trick libraries (C/C++)
trick_sims/      - example simulations
test/            - unit and integration tests
```
