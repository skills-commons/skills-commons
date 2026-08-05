# Skill format specification (v1)

A skill is a folder named in kebab-case containing at least `SKILL.md`.

## SKILL.md

YAML frontmatter, then the method in markdown:

```markdown
---
name: my-skill-name            # kebab-case, matches the folder
description: >-                # third person; states WHEN to use it
  One or two sentences. "Use when ..." triggers help assistants
  activate the skill at the right time.
version: "1.0.0"               # semver, quoted string
license: Apache-2.0
---

# Human-readable title

Role and stance (1–2 lines): who the assistant becomes.

## Inputs
What to ask the user for, what to assume, what is optional.

## Method
Numbered steps or checks. Concrete verbs. State how to degrade when a
tool or input is unavailable — "mark N.A. with a reason, never guess".

## Output format
The exact structure of the deliverable.

## Rules
Hard constraints, stated once, at the end.
```

## Requirements

1. **Self-contained**: no external fetches of further instructions, no
   URLs the agent must download to "complete" the skill, no encoded or
   obfuscated content of any kind.
2. **Readable**: plain markdown/text. If a reviewer can't read it, it
   doesn't merge.
3. **Honest degradation**: every step that depends on a tool (web access,
   file system, code execution) says what to do without it.
4. **Deterministic references**: counts and lists inside the skill must
   match themselves (a "12-step method" has 12 steps — reviewers count).
5. **No secrets handling**: skills never ask users for credentials, API
   keys, or personal data beyond what the task strictly needs.
6. **English body** for the library (assistants localize output);
   translated variants are welcome as `SKILL.<lang>.md` alongside.

## Optional files

- `README.md` — usage notes, examples of invocation.
- `CHANGELOG.md` — required from the first change after 1.0.0.
