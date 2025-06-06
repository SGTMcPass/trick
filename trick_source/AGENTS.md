# Trick Source Agent

Rules in this file apply to all C and C++ code inside `trick_source/`.

## Scope
```
codegen/       - Code generation tools
sim_services/  - Core simulation services
trick_utils/   - Utility libraries
trick_swig/    - SWIG interfaces
web/           - Web server and dashboard
```

## Coding Style
- Indent with **4 spaces**.
- Place opening braces on the same line as control statements and function definitions.
- Use C++ style comments `//` or block comments `/* */` as in existing files.
- Prefer standard library containers and algorithms when possible.
- Keep functions short and focused.

### Template
Header (`.hh`):
```cpp
#ifndef MY_CLASS_HH
#define MY_CLASS_HH

class MyClass {
public:
    MyClass();
    ~MyClass();
};

#endif
```
Source (`.cpp`):
```cpp
#include "MyClass.hh"

MyClass::MyClass() {}
MyClass::~MyClass() {}
```

## Common Actions
- Build and run the test suite with `make test` from the repository root.
- Unit tests may exist under each component's `test` directory and are built through their Makefiles.

## Verification Questions
1. Does new code follow the 4-space indentation and brace placement rules?
2. Are header include guards present and unique?
3. Are unit tests or regression tests updated when functionality changes?
4. Was `make test` executed after the changes?
5. Do commit messages reference relevant issue numbers when applicable?
