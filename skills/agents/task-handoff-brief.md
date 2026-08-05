---
name: task-handoff-brief
description: >-
  Builds a complete handoff brief for passing work between people or to
  an AI agent: goal, context, constraints, definition of done, and what
  to do when stuck. Use when delegating a task, briefing a colleague, or
  writing instructions another agent will execute unsupervised.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Task Handoff Brief

A handoff fails at the gap between what the giver assumed and what the
receiver understood. You write the brief that closes that gap before
work starts, for human and machine receivers alike.

## Inputs

1. The task as the giver describes it (required), in any state of mess.
2. Who or what receives it (colleague, contractor, AI agent) and what
   they already know about the context.
3. Deadline and priority relative to the receiver's other work.

## Method

1. **Extract the actual goal** — the outcome, stated as a verifiable
   result ("customers can reset passwords from the login page"), never
   as activity ("work on the reset flow"). Push back once when the
   stated task hides the real goal.
2. **Write the context floor**: the 3–7 facts the receiver must know to
   make sensible micro-decisions alone — why now, what was tried, what
   neighboring work this touches.
3. **State constraints separately from preferences.** Constraints are
   binding (budget, deadline, tools, approvals); preferences are
   defaults the receiver may override with reason. Mixing them is the
   top cause of both rework and paralysis.
4. **Define done as a checklist** the receiver can self-verify: outputs,
   quality bar, where the result lands, who gets told.
5. **Write the escape hatch** — the two or three situations where the
   receiver should stop and ask instead of pushing on, and exactly whom
   to ask. For AI receivers this section is mandatory and concrete
   ("stop and report when a step requires credentials you lack").
6. **Size check**: a brief the receiver reads in under three minutes.
   Longer means the task wants splitting — say so and propose the split.

## Output format

The brief, ready to paste, with these headings: Goal · Context ·
Constraints · Preferences · Definition of done · When to stop and ask ·
Deadline & priority.

## Rules

- Every item in Definition of done must be checkable by the receiver
  without asking the giver.
- Name things the receiver can access (files, systems, people); a brief
  that references "the usual doc" hands off confusion.
- One brief, one task: bundled tasks get separate briefs with an order.
