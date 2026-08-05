---
name: changelog-writer
description: >-
  Turns a span of commits, merged PRs, or a diff between tags into a
  Keep-a-Changelog-style entry: grouped by change type, written for
  humans, breaking changes impossible to miss. Use at release time or
  when a CHANGELOG.md has fallen behind reality.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Changelog Writer

A changelog answers one question per release: "what happens to me when
I upgrade?" You write for the developer consuming the project, never
for the team that built it — the git log already serves the team.

## Inputs

1. The raw material (required): commit list between two refs, merged
   PR titles/descriptions, or a diff summary. State what you received.
2. The version number and date, or the instruction to propose a bump
   (then apply semver logic from the changes: breaking → major,
   feature → minor, fix → patch — proposal, human decides).
3. The existing CHANGELOG.md when available: match its format
   exactly; absent one, use Keep a Changelog structure and say so.

## Method

1. **Classify every change** into: Added, Changed, Deprecated,
   Removed, Fixed, Security. Internal-life commits (refactors with
   zero behavior change, CI tweaks, test-code changes, dependency
   bumps with zero user impact) are filtered out and listed in a
   one-line "internal changes: N commits" note — presence
   acknowledged, attention spared.
2. **Rewrite each surviving entry from the consumer's seat**: what
   the user can now do, must now do, or will no longer suffer —
   never the implementation ("Fixed: date parsing crashed on
   timezone-less ISO strings", never "fixed the regex in
   dateutil.js"). One line per entry; a second line is allowed
   exclusively for migration instructions.
3. **Surface the breaking changes twice**: in their category with a
   **BREAKING** prefix, and in a dedicated block at the top of the
   release entry with the migration step for each. A breaking change
   the reader can miss is the single failure this format exists to
   prevent.
4. **Credit and reference** per house style: PR/issue numbers linked
   where the existing changelog links them; contributor credit where
   the project practices it.
5. **Cross-check completeness**: every commit/PR from the input is
   either represented in an entry or covered by the internal-changes
   note — state the reconciliation count (e.g. "47 commits → 12
   entries + 31 internal + 4 reverts cancelling out").

## Output format

The release section, ready to paste at the top of CHANGELOG.md:
`## [x.y.z] - YYYY-MM-DD`, breaking block when applicable, then the
populated categories (empty categories omitted), then the internal
note. Plus, separately: the semver-bump rationale when a bump proposal
was requested.

## Rules

- Consumer perspective is the invariant: any entry starting with a
  developer-facing implementation detail gets rewritten or filtered.
- The reconciliation count ships every time — a changelog that
  silently dropped commits is a changelog nobody can trust again.
- Chronology inside a category is by impact, never by commit date.
- Yanked or reverted-within-the-span changes appear nowhere except
  the reconciliation note: shipping a feature and its revert as two
  entries is noise wearing a suit.
