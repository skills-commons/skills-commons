---
name: readme-architect
description: >-
  Builds or rebuilds a repository README that answers the visitor's
  three questions in order: what is this, is it for me, how do I start.
  Use for new repos, READMEs that grew by accretion, or projects whose
  issue tracker keeps answering questions the README should.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# README Architect

A README has ninety seconds before the visitor leaves. You spend them
in the visitor's order of need — what, whether, how — and you treat
every support question the maintainers keep re-answering as a README
bug to fix here.

## Inputs

1. The repository (required): code layout, manifest files, existing
   README, docs folder — whatever is available. State what you read.
2. The audience: library consumers, app end-users, contributors,
   evaluators-before-adoption. Multiple audiences = explicit sections,
   ordered by traffic.
3. Recurring questions (optional, gold): the issues or support
   messages that keep coming back.

## Method

1. **Write the opening block** — the make-or-break screen: project
   name; one sentence saying what it does and for whom (concrete
   nouns, zero adjectives); 3–5 lines showing the thing actually
   working (the killer example: real input → real output); badges
   limited to the ones that inform a decision (CI, version, license).
2. **The "is it for me" section**: what problems it solves, what it
   deliberately leaves out, and the honest comparison line when a
   well-known alternative exists ("choose X when you need Y; choose
   this when you need Z"). Stating what the project is NOT for saves
   both sides a week.
3. **Quickstart** — the shortest verified path from zero to first
   success: prerequisites with versions, install command, minimal
   working example, expected output shown verbatim. Every command
   must be runnable as written (no placeholder soup); when
   verification is possible in the environment, run them; otherwise
   mark the quickstart "written from the docs, verify on a clean
   machine".
4. **The depth ladder**, in descending traffic order: configuration
   (the 5 options people actually change, table format; the full
   reference gets a link, never an inline dump), common recipes (one
   per recurring question from the inputs), troubleshooting (symptom →
   cause → fix, from real issues), contributing pointer, license line.
5. **Prune what a README must never hold**: API reference dumps,
   changelogs, roadmaps, philosophical essays — each gets a one-line
   pointer to its proper home. A README is a lobby, never the whole
   building.
6. **Self-check against the three questions**: a stranger reading the
   first screen can say what this is; the second screen, whether it's
   for them; the third, they have it running. Any failure → restructure
   before polishing sentences.

## Output format

The complete README.md, ready to commit, plus a 3-line delivery note:
what was cut and where it moved, which quickstart commands were
verified vs written-from-docs, and which recurring questions got a
section.

## Rules

- The killer example is real: runnable input, actual output — a
  fabricated output block is the fastest way to lose a developer
  forever.
- Order by visitor traffic, never by team pride: architecture
  diagrams live below quickstart, always.
- Version-pinned claims ("requires Node ≥ 20") come from the manifest,
  never from memory; unverifiable claims are marked.
- One screen, one job: any section serving two audiences splits.
