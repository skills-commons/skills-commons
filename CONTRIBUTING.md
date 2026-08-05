# Contributing

A merge here means a human checked your skill line by line. That review is
what makes this library worth installing from — thank you for going
through it.

## What belongs here

Professional methods for AI assistants: tasks people re-explain to their
AI every day, packaged once, well. Generic craft only — no skills that
require or reveal proprietary systems, no vendor-specific hacks, no
content that needs credentials to demonstrate.

## How to submit

1. Read [SPEC.md](SPEC.md) and mirror an existing skill's structure.
2. One skill per pull request, in `skills/<your-skill-name>/`.
3. Fill the PR template checklist (it mirrors [SECURITY.md](SECURITY.md)).
4. Expect real review: questions about ambiguous steps, requests to count
   your own checklist, pushback on vague verbs. Two passing reviews
   (quality + security) merge it.

## The quality bar

- **Executable, honestly**: an assistant with common tools can follow
  every step; steps that need special tools declare their fallback.
- **Direct**: no motivational filler, no repeated framing. Every sentence
  either instructs or constrains.
- **Self-consistent**: declared counts match actual items; the output
  format section matches what the method produces.
- **Tested**: you ran it at least once on a real case and the PR
  description says what happened.

## Credit

Contributors are listed in the skill's frontmatter (`authors:`) and in
release notes. By submitting, you license your contribution under
Apache-2.0.

## Maintainers

Seeded and maintained by AGORÀ Intelligence. Maintainer decisions aim for
the library's trust first; when in doubt, we decline politely and explain
why.
