# Skill format specification (v1)

A skill is a single markdown file named in kebab-case after the skill itself, placed in its category folder: `skills/<category>/<skill-name>.md`. With hundreds of skills per category ahead, identifying filenames are the rule — a repository of files all named SKILL.md is unsearchable.

The [Agent Skills specification](https://agentskills.io/specification)
instead defines a skill as a directory holding a `SKILL.md`. Both shapes
ship: `tools/build_dist.py` converts this one into that one, so the
source stays searchable and the artefact stays installable.

## The file

YAML frontmatter, then the method in markdown:

```markdown
---
name: my-skill-name            # kebab-case, matches the filename
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
   translated variants are welcome as `<skill-name>.<lang>.md` beside the
   original.

## Companion files

The layout is flat, so a skill has no folder of its own to put things in.
Companions carry the skill's name and say what they are:

- `<skill-name>.CHANGELOG.md` — required from the first change after
  1.0.0, beside the skill it describes.
- Usage notes and invocation examples belong inside the skill file, not
  in a separate README.
