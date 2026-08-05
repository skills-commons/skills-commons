---
name: note-organizer-pro
description: >-
  Turns chaotic notes, braindumps or scattered thoughts into structure:
  themes, actions, decisions, open points. Use when handed messy notes
  and asked to organize, structure, or "make sense of this".
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Note Organizer Pro

You bring order to raw thinking while respecting it: organizing means
finding the structure already latent in the notes, never replacing their
substance with your own.

## Inputs

1. The notes (required) — any format, any mess.
2. Purpose, when stated: prepare a meeting, plan a project, clear the
   head. No purpose? Organize for retrieval (default).

## Method

1. Read everything once without organizing — messy notes often bury the
   key item near the end.
2. Tag every fragment with one primary bucket:
   - **Action** — something to do (owner and deadline when present).
   - **Decision** — something already settled.
   - **Idea** — worth keeping, needs development.
   - **Question** — open, needs an answer or a person.
   - **Fact/Reference** — data, names, links, constraints.
   - **Duplicate/noise** — repeated or empty fragments; count them,
     drop them.
3. Within buckets, cluster by theme, naming each cluster with words taken
   from the notes themselves (the author's vocabulary beats yours).
4. Surface what the author couldn't see in the mess:
   - actions repeated in different words (a signal of importance),
   - contradictions between fragments,
   - questions the notes actually answer elsewhere.
5. Preserve original wording where it is sharp; rewrite where it is
   broken. Rewritten fragments are marked with °.

## Output format

1. **In one look** — 3 lines: what these notes are about, the most urgent
   action, the most important open question.
2. **Actions** — table: what · owner · deadline · source fragment.
3. **Decisions**, **Ideas** (clustered), **Questions**, **References** —
   each bucket only when it has content.
4. **Signals** — repetitions, contradictions, self-answered questions.
5. One closing line: fragments processed / dropped as noise.

Write in the language of the notes.

## Rules

- Nothing invented, nothing silently lost: dropped fragments are counted.
- Cluster names come from the author's own words.
- Marks (°) make every rewrite visible.
