# Simulations Agent

This file governs all example simulations under `trick_sims/`.

## Scope
All directories inside `trick_sims/` including nested `SIM_*` folders and sub-projects such as `Ball/SIM_ball_L1` follow these rules.

### Directory Pattern
A typical simulation contains the following items:
```
SIM_name/
    S_define           - build configuration macros
    S_overrides.mk     - additional make flags
    Modified_data/     - Python scripts for real‑time settings
    RUN_*/             - scenario directories with `input.py` and optional `unit_test.py`
    models/            - C/C++ model sources
    README.md          - usage notes
```

## Coding Style
- C/C++ source under `models/` follows the conventions in `/trick_source/AGENTS.md`.
- Python scripts follow `/share/trick/pymods/trick/AGENTS.md`.
- Markdown documents follow `/docs/AGENTS.md`.
- Keep `S_define` comments in the same style as existing examples.

## Common Actions
- Build a simulation with `make` from its directory or from `trick_sims`.
- Clean artifacts with `make spotless`.
- Run the simulation using `S_main_*.exe RUN_test/input.py` or another RUN directory.
- Some sims include graphics clients built under `models/graphics/` with `make`.

## Template
Use this skeleton when creating a new simulation:
```
SIM_example/
    models/
        example/src/Example.cpp
    S_define
    S_overrides.mk
    Modified_data/
        realtime.py
    RUN_test/
        input.py
        unit_test.py
    README.md
```

## Verification Questions
1. Does each simulation directory include `S_define` and `S_overrides.mk`?
2. Do new C/C++ files comply with the Trick Source Agent's style rules?
3. Are Python scripts PEP8 compliant and covered by `unit_test.py` when applicable?
4. Was the simulation built with `make` and executed using a RUN directory before committing?
5. Are README or documentation updates written in Markdown using the docs style guide?
