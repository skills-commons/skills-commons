---
name: issue-triage-pro
description: >-
  Triages a batch of repository issues: duplicates linked, missing
  reproduction info requested with a specific ask, severity and labels
  proposed, the response drafted for each. Use on issue-tracker
  backlogs, after a release wave, or as a recurring inbox-zero pass.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Issue Triage Pro

An untriaged tracker punishes exactly the users who bothered to write.
You turn a pile of issues into a labeled, deduplicated, answered queue
— and every reporter gets a response that proves a human-quality
reading happened.

## Inputs

1. The issues (required): pasted list, export, or tracker access.
2. The project's label taxonomy and severity conventions when they
   exist; otherwise propose a minimal set (bug / feature / question /
   docs; severity by user impact) and use it consistently.
3. Known hot spots (optional): current release problems, deprecated
   areas, the FAQ answers that keep being re-asked.

## Method

1. **Classify each issue**: bug report / feature request / question /
   docs gap / unclear. The unclear ones get the sharpest treatment —
   see step 3.
2. **Hunt duplicates across the batch and against known issues**: same
   root symptom under different words (error text match, same
   component + same trigger). Link duplicates to the canonical issue
   (oldest with the best information, or the best-documented one —
   say which rule you applied), and carry any NEW information from
   the duplicate into the canonical thread instead of losing it.
3. **Gate bug reports on reproducibility**: environment, steps,
   expected vs actual. Missing pieces produce a request that names
   exactly what is missing and why it unblocks the fix ("which
   database version — the fix differs before/after 14") — never the
   generic "please provide more info" that trains reporters to stop
   reporting.
4. **Rate severity by user impact** (data loss > blocked task > wrong
   result > friction > cosmetic) × spread (everyone / a segment / one
   setup). Flag the quiet criticals: low-noise issues describing data
   corruption outrank loud cosmetic threads, and the triage says so.
5. **Draft the response for every issue**, in the project's tone:
   thanks proportional to effort invested by the reporter, what was
   understood (one line proving the reading), what happens next or
   what is needed, the label/severity applied. Questions answered by
   docs get the link AND the one-line answer — the link alone reads
   as a brush-off, and the docs gap gets its own issue when the
   question keeps recurring.

## Output format

**Triage table**: issue, type, duplicate-of, severity, labels,
next-action owner (maintainer / reporter / stale-close candidate) ·
**Drafted responses**, one per issue, ready to paste · **Patterns
note**: clusters the batch reveals (one component generating 40% of
reports, a docs page that would kill five questions) — the triage's
strategic output. Stale-close candidates carry the grace-period
message, never a silent close.

## Rules

- Every duplicate link states the matching evidence (shared error
  line, same trigger); "seems similar" closes nothing.
- No issue closes without a response a reasonable reporter would
  accept as an answer.
- Severity follows user impact, never fix difficulty — easy-to-fix
  and critical are independent axes, and conflating them is how data
  loss waits behind typo fixes.
- The patterns note ships every time: triage that fixes the queue and
  ignores what the queue is saying does half the job.
