# Documentation Agent

This file governs all documentation under `docs/` including `developer_docs`, `documentation`, `howto_guides`, and related assets.

## Scope
Any Markdown (`.md`) or documentation specific configuration inside this directory tree follows these rules.

### Directory Outline
```
developer_docs/    - Internal developer information
howto_guides/      - Step by step guides for users
documentation/     - Main user documentation
_layouts/          - Jekyll layouts for the website
```

## Style Guidelines
- Use GitHub Flavored Markdown.
- Begin each document with a top level `# Title` followed by a short introductory paragraph.
- Wrap lines at 120 characters or less for readability.
- Use relative links when referring to other files in this repository.
- Prefer fenced code blocks with language hints: <code>```python</code>, <code>```cpp</code>, etc.

### Template
Use the following skeleton for new documents:
```markdown
# Title

Short summary of the page purpose.

## Overview
Describe the workflow or concept.

## References
- [Related Document](../path/to/doc.md)
```

## Verification Questions
1. Does the new documentation follow the heading and line length conventions?
2. Are cross references written with relative paths?
3. Is the writing concise and free of obvious grammar issues?
4. Are code blocks properly fenced with language identifiers?
5. Have spelling and formatting been checked before commit?
