---
name: decision-record
description: >-
  Records a decision so the next person understands it without asking:
  what was chosen, what was rejected and why, what would reverse it. Use
  for architecture and product decisions, for meetings that ended in a
  choice, or when a past decision is being relitigated from memory.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Decision Record

You write the document that stops a decision being made twice. The value
sits in the rejected options and the conditions that would change the
answer, because those are what nobody remembers six months later.

## Inputs

1. The decision (required): what was chosen, however roughly stated.
2. The alternatives that were considered. When none are offered, ask once
   — a decision with no alternatives is either trivial or unexamined, and
   the answer tells you which.
3. The forces: constraints, deadlines, costs, people affected.
4. Who decided and when. Absent, mark the owner as unassigned and say so
   in the record rather than guessing a name.

## Method

1. **State the decision in one sentence**, in the active voice, naming
   the thing chosen. "We will use X for Y." A record whose first line
   needs a second line has not decided anything yet.
2. **Write the forces before the options.** What was true that made this
   a question: the load that broke, the deadline, the budget, the skill
   the team lacks. A reader who disagrees with the decision usually
   disagrees with a force, and this is where they find it.
3. **List every option that was live**, including the one nobody liked,
   with one line each on what it would have cost. Options invented after
   the fact to make the choice look inevitable are worse than none.
4. **Say why the chosen option won**, against the forces in step 2 and
   not in the abstract. "Cheaper" is a claim; "cheaper by roughly 40% of
   the annual licence, which was the binding constraint" is a reason.
5. **Name the price paid.** Every decision costs something: latency,
   flexibility, a dependency, a skill the team must now learn. A record
   with no downside reads as advocacy and gets trusted accordingly.
6. **State what would reverse it** — the measurement, threshold or event
   that should reopen the question. This is the single most useful line
   in the document and the one most often missing.
7. **Set the status**: proposed, accepted, superseded by another record.
   Records are never edited into agreement with the present; a changed
   mind is a new record that supersedes this one.

## Output format

A one-page record, in this order: title and status, the decision in one
sentence, context and forces, options considered with their costs, the
reasoning, the consequences including what was given up, and the
reversal condition. Date and decider at the top. Numbered so it can be
referenced: `0001`, `0002`, and so on.

## Rules

- The rejected options stay in the document forever. Deleting them turns
  a record into a justification.
- Every claim of cost or benefit is either quantified or marked as an
  estimate. Confidence and precision are not the same thing.
- What was unknown at the time is written as unknown, in the present
  tense of the decision. A record that hides its uncertainty teaches the
  reader that the team is never uncertain.
- No editing to match what happened next. Supersede instead.
