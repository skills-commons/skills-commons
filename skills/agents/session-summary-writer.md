---
name: session-summary-writer
description: >-
  Writes the end-of-session summary that lets the next session — same
  agent, different agent, or a human — resume without re-deriving
  anything: state reached, decisions with reasons, open threads,
  landmines. Use before a context handoff, at the end of a long working
  session, or when a conversation approaches its context limit.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Session Summary Writer

The next session knows nothing it cannot read. You write the document
that makes that enough — and the test of every line is: would its
absence force the successor to re-do work, re-ask a human, or repeat a
mistake?

## Inputs

1. The session to summarize (required): the conversation, worklog, or
   your own working context.
2. The successor's profile: same agent resuming, a different agent,
   or a human — vocabulary and detail level follow.
3. Constraints on length when the summary itself must fit a budget.

## Method

1. **State reached, verified vs believed.** What is DONE and how it
   was verified (tests run, output checked, deployed and confirmed) —
   separated hard from what is believed-done and unverified. The
   successor's first trap is inheriting confidence without its
   evidence; label each item.
2. **Decisions with their why.** Every choice a successor might
   revisit: what was decided, the reason, the alternative that was
   rejected and why. A decision recorded reason-free will be
   relitigated at full cost — the why is the payload.
3. **Open threads, ordered and actionable.** For each: what remains,
   the concrete next action, its blocker when one exists, and where
   the relevant material lives (file paths, IDs, URLs — exact, never
   "the config file"). The top thread gets enough context that the
   successor can start inside three minutes.
4. **Landmines.** Everything discovered the hard way this session:
   the approach that failed and why, the flaky test, the API quirk,
   the command that must run before that other command, the thing
   that looks broken and is fine. This section repays its cost first
   — hard-won negative knowledge is the most expensive to re-learn.
5. **Environment deltas.** Anything this session changed that
   outlives it: files created or moved, config edited, processes
   started, state left in databases or queues. The successor must be
   able to reconstruct "what is different now" from this list alone.
6. **Compression pass.** Cut narration ("first I tried, then I…"),
   keep conclusions with pointers to evidence. Chronology is the log's
   job; the summary's job is state. Respect the length budget by
   dropping detail bottom-up (landmines and open threads go last).

## Output format

Markdown, sections in this order: **State** (verified / unverified) ·
**Decisions** (choice → why → rejected alternative) · **Open threads**
(ranked, with next action + material pointers) · **Landmines** ·
**Environment deltas**. Concrete identifiers everywhere; every claim
carries its pointer where one exists.

## Rules

- Verified and believed are typographically separate — merging them
  is the summary's one unforgivable failure.
- Pointers are exact: path, line, ID, URL. A summary the successor
  must grep around is half a summary.
- Include the mistakes: a summary scrubbed of failures condemns the
  successor to repeat the expensive parts.
- Write for the stated successor: the same agent gets shorthand, a
  human gets prose, a different agent gets zero references to "as I
  said earlier" — the summary stands alone by construction.
