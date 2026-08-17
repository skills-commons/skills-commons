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
audience: public               # optional; see "Output written for publication"
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
7. **Output written for publication declares itself.** A skill whose
   deliverable is meant to be published — an article, a press release, a
   product page, a post — sets `audience: public` in the frontmatter and
   carries a `## Disclosure` section telling the user that the result must
   be marked as AI-authored, citing **EU AI Act art. 50**. The field is
   opt-in: a skill that writes for an internal reader sets `audience:
   internal` or omits the key, and nothing is required of it. What is not
   negotiable is the pairing — declaring `public` without the section is a
   lint error, because the claim and the obligation must travel together.

## Output written for publication

Article 50 obliges whoever puts AI-generated content in front of the public
to say so. A skill cannot enforce that on the person using it, and pretending
otherwise would be theatre. What it can do is refuse to let the obligation go
unmentioned: the method that drafts the article is also the place where the
reader learns the article needs a notice.

The disclosure names an **organisation**, never an invented person. A skill
that instructs the assistant to sign work with a fictional human byline does
not merge here.

## Companion files

The layout is flat, so a skill has no folder of its own to put things in.
Companions carry the skill's name and say what they are:

- `<skill-name>.CHANGELOG.md` — required from the first change after
  1.0.0, beside the skill it describes.
- Usage notes and invocation examples belong inside the skill file, not
  in a separate README.
