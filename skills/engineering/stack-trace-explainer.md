---
name: stack-trace-explainer
description: >-
  Reads a stack trace or error dump and returns the story: what broke,
  where it actually originated (versus where it surfaced), the most
  likely causes ranked, and the next diagnostic step for each. Use when
  handed an unfamiliar traceback, a production error, or a wall of log
  noise around one failure.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Stack Trace Explainer

A stack trace tells the truth in an unhelpful order. You re-tell it in
the useful order: origin before surface, cause hypotheses before code
tours, the next step before the lecture.

## Inputs

1. The trace or error output (required) — any language, any format,
   including mixed log noise around it.
2. Context when available: what action triggered it, how often it
   fires (always / intermittent / once), what changed recently
   (deploy, dependency bump, config, data), runtime versions.
3. The relevant source code, when shareable — turns hypotheses into
   verdicts.

## Method

1. **Isolate the failure from the noise.** In mixed logs, identify
   the actual exception chain: the innermost/root error (in
   `Caused by:` chains, `__cause__` chains, wrapped errors — the
   deepest one is usually the story), versus the framework's
   re-raise ceremony around it. Quote the exact error line and name
   the error class in plain words.
2. **Split the frames into three zones**: your code (the frames that
   matter), the libraries in between (usually innocent conduits),
   the runtime/framework bootstrap (ignorable ceremony). Point to the
   **last your-code frame before the error** — the true crime scene —
   which is routinely far from the line that surfaced the error.
3. **Rank the causes.** From the error class + crime-scene frame +
   context, list the 2–4 most likely causes, ordered by probability,
   each with: the mechanism in one sentence, the evidence in the
   trace that supports it, and **the one diagnostic step that would
   confirm or kill it** (a log line to add, a value to print, a
   request to replay, a version to check). Intermittent failures get
   the concurrency/data-dependent causes ranked honestly.
4. **Check the recent-change axis.** When context says something
   changed, test each hypothesis against the change first — most
   production traces are new-change × old-assumption collisions.
5. **Deliver the fix path, staged**: the immediate mitigation when
   one exists (guard, retry, rollback — labeled as mitigation), then
   the root fix per the leading hypothesis, then the regression test
   that would have caught it. When source was provided and the cause
   is a verdict rather than a hypothesis, say so and show the line.

## Output format

**What broke** (one sentence, plain words) · **Where it originated**
(file:line of the crime-scene frame, quoted) · **Ranked causes** (2–4,
each: mechanism, evidence, confirming step) · **Fix path** (mitigation
/ root fix / test) · **What I could rule out** from the trace alone,
stated. Length proportional to the mystery: an obvious null-reference
gets ten lines, never a report.

## Rules

- Hypotheses are labeled as hypotheses until source or a diagnostic
  confirms them — a confident wrong cause costs the reader hours in
  the wrong file.
- Every cause comes with its kill test: analysis that leaves the
  reader with "interesting, now what" has failed.
- Version-specific claims ("this changed in Django 5.1") are stated
  as from-memory and flagged for verification unless docs were
  checked live.
- The trace is quoted, never paraphrased, in the origin section —
  paraphrased errors are unsearchable.
