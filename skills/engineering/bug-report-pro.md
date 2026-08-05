---
name: bug-report-pro
description: >-
  Turns "it's broken" into a bug report that gets fixed on the first
  pass: minimal reproduction steps, environment, expected vs. actual,
  severity, and evidence. Use when reporting a bug, triaging a vague
  user complaint, or reviewing a report before it reaches engineers.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Bug Report Pro

A bug report is a reproduction recipe with evidence attached. You write
reports an engineer can act on before their coffee cools, and you refuse
to file vagueness upward.

## Inputs

1. What happened, in the reporter's words (required) — including logs,
   screenshots, error text when available.
2. Where it happened: product area, URL or screen, and rough time.
3. Environment as far as known: OS, browser/app version, account type,
   network conditions.

## Method

1. **Reduce to minimal reproduction.** From the reporter's story, strip
   every step that also leads to the bug when removed. Number the steps
   from a state anyone can reach ("logged out, empty cart"). When the
   story lacks the trigger, list the 2–3 most likely repro paths as
   explicit hypotheses to test.
2. **Split expected from actual.** Expected comes from documentation,
   UI promise, or reasonable convention — name which. Actual is what
   observably happened, quoted or screenshotted, timestamps kept.
3. **Pin the environment** — every axis known, "unknown" written where
   it applies. An unstated environment is the leading cause of
   "works on my machine" round-trips.
4. **Rate severity by user impact** (data loss > blocked task > wrong
   result > friction > cosmetic) and note scope: one user, a segment, or
   everyone. Frequency and workaround existence go here.
5. **Attach the evidence inventory**: what exists (log excerpt, HAR,
   screen recording), where it lives, what the engineer would likely
   ask for next — offer to gather it now.
6. **Title last**: symptom + area + condition, greppable, under 80
   characters ("Checkout: 500 on order submit when coupon field left
   empty").

## Output format

Title · Steps to reproduce (numbered, from clean state) · Expected ·
Actual · Environment · Severity & scope · Evidence · Regression note
(worked before? when?) · Open questions.

## Rules

- One bug per report; a second symptom becomes a second report with a
  cross-link.
- Facts and hypotheses live in separate sections — a guessed root cause
  presented as fact derails triage.
- Quote errors verbatim; paraphrased error text is unsearchable.
- Reports about intermittent bugs state the observed frequency ("3 of
  ~20 attempts") — "sometimes" is data thrown away.
