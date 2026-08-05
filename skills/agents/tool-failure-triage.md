---
name: tool-failure-triage
description: >-
  Diagnoses a failed tool call, API request, or command before retrying:
  classifies the failure, picks the response strategy (retry, adapt,
  work around, escalate), and prevents the retry-identical-forever
  loop. Use when an agent's action fails, especially twice.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Tool Failure Triage

Retrying an unchanged call against an unchanged failure is the most
common way agents burn budgets. You stand between the failure and the
retry, and you let the retry through exclusively when the diagnosis
says the world — or the call — has changed.

## Inputs

1. The failed action (required): the call as made, verbatim, and the
   complete error output — message, code, status, stderr.
2. The attempt history: how many tries, what varied between them.
3. The goal the action serves — the workaround search needs it.

## Method

1. **Read the error, actually.** Quote the decisive line and classify:
   - **Transient** (timeout, 429, 5xx, connection reset, resource
     busy): the world may change on its own → retry is legitimate,
     with backoff and a retry budget.
   - **Deterministic — the call is wrong** (4xx, validation error,
     parse error, wrong path, missing argument, auth failure): the
     identical call fails identically forever → retry is prohibited
     until the call changes.
   - **Deterministic — the world is wrong** (missing dependency, file
     locked by design, permission denied, quota exhausted): fix the
     precondition or route around; retrying the call touches neither.
   - **Ambiguous** (empty error, generic "failed"): one — one —
     diagnostic probe designed to split the cases (a smaller call, a
     dry-run flag, a read of the state the call assumed), then
     reclassify.
2. **Compare across attempts** when history exists: same error twice
   with the same call = deterministic by evidence, whatever the
   message claims. An error that CHANGED between attempts is
   information — diagnose the delta before anything else.
3. **Pick the strategy by class**: transient → bounded retries
   (suggested: 3, exponential backoff, then treat as deterministic);
   call-wrong → fix the specific defect the error names, then one
   retry; world-wrong → precondition fix or workaround; ambiguous →
   probe, reclassify, proceed.
4. **Search the workaround honestly** when the direct path stays
   blocked: alternative tool, alternative route to the same goal,
   partial result worth having. A workaround that silently delivers
   less than the goal is reported as partial, never passed off as
   done.
5. **Escalate well when escalation wins.** When the diagnosis says
   human input is needed (credentials, permissions, a judgment call),
   stop and report: what was attempted (calls verbatim), the decisive
   error line, the diagnosis, what was tried, the specific thing
   needed to proceed. An escalation carrying its evidence gets
   answered in minutes; "it failed" gets answered with questions.

## Output format

**Diagnosis**: class + the quoted decisive line · **Strategy**: what
happens next and why this beats blind retry · **Action**: the fixed
call / the probe / the workaround / the escalation report · **Budget
note**: attempts used, attempts remaining before strategy changes.
Compact — triage serves the task, and a ten-line triage that saves
forty retries is the point.

## Rules

- The identical call is retried exclusively on transient diagnoses,
  inside a stated budget — everything else changes the call or the
  world first.
- Every diagnosis quotes the error's decisive line; triage built on a
  paraphrase inherits the paraphrase's errors.
- Probes are minimal and read-only where possible; a diagnostic that
  mutates state is a second incident waiting.
- Partial results are labeled partial. The failure report is a
  deliverable, and its honesty is what makes the next attempt
  cheaper.
