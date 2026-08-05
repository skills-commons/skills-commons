---
name: honest-status-report
description: >-
  Produces status reports that declare failures, blockers and partial
  results as visibly as successes. Use for project status updates,
  work summaries, or any "how is it going" report — human or AI-agent
  work alike.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Honest Status Report

You write status the way an engineer reads instruments: what happened,
what failed, what is unknown — before what went well. A report that hides
a failure costs more than the failure.

Born from a pattern observed in production AI agents: errors silently
suppressed behind a green "done" until the fourth one mattered. This
skill is the antidote, and it works for human status reports too.

## Inputs

1. The raw material: work log, ticket list, commit history, agent
   transcript, or a verbal account (required).
2. Audience and cadence: teammate daily, manager weekly, client monthly.
3. The previous report, when available (enables deltas and promise
   tracking).

## Method

1. Inventory everything attempted in the period — including work started
   and abandoned. Abandonment is status.
2. Classify each item, strictly:
   - **Done & verified** — completed AND checked. State how it was
     verified in a few words. Unverified completion goes below, honestly.
   - **Done, unverified** — finished on paper; verification pending.
   - **Partial** — progress with a measurable fraction or milestone.
   - **Failed / errored** — attempted, went wrong. What, why (when
     known), what was retried.
   - **Blocked** — stopped by an external dependency: name it and name
     the unblock owner.
   - **Silently skipped** — planned, then untouched. The easiest category
     to omit and the most important to keep.
3. Track promises: anything committed in the previous report that moved
   or vanished gets one explicit line.
4. Write risks forward: the two things most likely to bite next period,
   each with the early signal to watch.

## Output format

1. **Headline** — one sentence, plain truth ("on track except X", "two
   failures need decisions").
2. **Needs attention** — failures, blockers, skipped items. FIRST, every
   time, even when empty ("no failures to report" is a statement, earned).
3. **Done & verified** / **In progress** — compact lists with evidence.
4. **Promise check** — deltas vs previous report.
5. **Next period + risks** — commitments with dates, risks with signals.

Length: fits the cadence (daily ≤ 10 lines; weekly ≤ 1 page).

## Rules

- The order is non-negotiable: problems before achievements.
- Every "done" states its verification or drops to "unverified".
- Numbers over adjectives: "3 of 5 endpoints migrated" beats "good
  progress".
