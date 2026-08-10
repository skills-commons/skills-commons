---
name: incident-postmortem
description: >-
  Turns an outage into a timeline, a set of contributing causes and
  changed defaults, without naming a culprit. Use after an incident,
  a near miss, or any failure whose explanation is currently "someone
  made a mistake".
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Incident Postmortem

You reconstruct what happened so the same conditions produce a different
outcome next time. Blame ends the investigation early, which is why it is
absent here: a system that fails when one person errs was already broken
before they touched it.

## Inputs

1. The incident (required): what broke, when it started, when it ended,
   who noticed and how.
2. The evidence: alerts, logs, dashboards, chat transcripts, deploy
   history. State which of these you received, because the timeline is
   only as good as its sources.
3. The impact: users affected, requests failed, money or data lost. When
   unmeasured, say unmeasured — an invented figure survives longer than
   the report.
4. The remediation already applied, if any.

## Method

1. **Build the timeline from timestamps, not memory.** Each entry: time,
   what happened, how it is known. Include the gap between the incident
   starting and anyone noticing — that gap is usually the finding.
2. **Separate the trigger from the conditions.** The deploy that broke it
   is the trigger. The absent test, the alert that only fires in business
   hours, the runbook nobody had run: those are the conditions, and they
   were there before the trigger arrived.
3. **Ask what made the response slow**, separately from what caused the
   failure. Detection, escalation and mitigation each have their own
   duration and their own fix. Collapsing them hides the cheapest
   improvement.
4. **List contributing causes, plural.** A single root cause is almost
   always the point at which the investigation stopped. For each, say
   what would have had to be different.
5. **Note what worked.** The alert that did fire, the rollback that was
   quick, the person who found it. Removing a working control because
   nobody noticed it working is its own future incident.
6. **Convert each cause into a changed default**, not a resolution to be
   careful. "Add a check that fails the deploy when the migration is
   irreversible" is a default; "review migrations more carefully" is a
   wish. Each gets an owner and a date, or it is recorded as unowned.
7. **Rate the remaining exposure**: if the same trigger fired tomorrow,
   what would happen now. This is the only honest measure of whether the
   postmortem accomplished anything.

## Output format

Summary in three lines — what broke, for how long, who was affected —
then impact with numbers, the timeline as a table, contributing causes,
what worked, actions with owners and dates, and the remaining exposure.
Written so someone outside the team can follow it without a glossary.

## Rules

- No names attached to mistakes. Roles and systems, never people. A
  report someone is afraid of is a report that gets sanitised next time.
- Every timeline entry carries its source. Entries that rest on
  recollection are marked as such.
- Unknowns stay unknown. "The cause of the initial latency spike was not
  determined" is a finding; a plausible guess written as fact is damage.
- An action without an owner and a date is listed as unowned rather than
  quietly implied to be handled.
- Impact figures are measured or labelled as estimates, always.
