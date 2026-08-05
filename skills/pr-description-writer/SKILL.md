---
name: pr-description-writer
description: >-
  Writes pull request descriptions that speed up review: the why, the
  what, the how-to-verify, and the risk surface, sized to the change.
  Use when opening a PR, or when a diff needs a description a reviewer
  can trust without reverse-engineering the code.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# PR Description Writer

The diff shows what changed; your description explains why, what to look
at first, and how to prove it works. You write for a reviewer with ten
minutes and three other PRs in queue.

## Inputs

1. The diff, branch, or list of commits (required).
2. The motivating context: ticket, incident, discussion — or the
   author's one-line reason.
3. How the author verified the change, when they did.

## Method

1. **Lead with the why**: the problem or need in 1–2 sentences, linked
   to its source (issue, incident, thread). A reviewer who knows the
   intent reviews twice as fast and catches design-level mistakes, the
   expensive kind.
2. **Summarize the what by behavior**, in bullets ordered by importance:
   user-visible changes first, then API/contract changes, then
   internals. Name the files worth reading first when the diff exceeds
   a screen.
3. **Write the verification recipe** — numbered steps a reviewer can run
   (setup, action, expected result), plus what the author already ran
   (tests added/updated, manual checks, staging link). "CI is green" is
   a floor, never the recipe.
4. **Declare the risk surface**: behavior changes, migrations, config or
   env changes, rollback path, and anything intentionally left out of
   scope with its follow-up.
5. **Match size to stakes** — a typo fix earns three lines; a migration
   earns the full template. Padding small PRs erodes trust in big ones.

## Output format

Markdown, ready to paste: **Why** · **What changed** · **How to
verify** · **Risk & rollback** · **Out of scope**. Prefixed with a
one-line summary usable as squash-commit message (imperative, ≤72
chars).

## Rules

- Every claim about behavior must be checkable via the diff or the
  verification steps.
- Breaking changes and migrations are named in the first screen, in
  bold — never below the fold.
- Write "how to verify" as commands and clicks, never "test the flow".
- The description mentions its own gaps ("no test for the retry path,
  needs a flaky-network harness") — hiding them wastes the reviewer's
  discovery on what the author already knew.
