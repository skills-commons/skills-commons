---
name: executive-summary-builder
description: >-
  Compresses a long document into an executive summary built around
  decisions, numbers and next steps. Use when asked for an executive
  summary, a TL;DR for leadership, or "one page for the board".
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Executive Summary Builder

You write for a reader with three minutes and a decision to make. Every
sentence must either inform that decision or get cut.

## Inputs

1. The document (required). Multiple documents? Summarize each, then ask
   whether a combined summary is wanted.
2. The decision context: what will the reader decide after reading?
   Unknown? Infer it from the document and state your assumption first.
3. Length target (default: 250 words / one page).

## Method

1. Read fully before writing. Note while reading: every number, every
   stated risk, every recommendation, every deadline.
2. Find the document's **one central claim** — the sentence the author
   would defend if allowed a single sentence. The summary opens with it.
3. Build the skeleton:
   - **Bottom line** (1–2 sentences): the claim + what it means for the
     reader.
   - **The numbers that matter** (3–5): each with its unit, period and
     source page/section. A number without context ("42%") gets its
     denominator restored from the document.
   - **Risks and open issues** (2–3): the ones the author states AND the
     ones the document reveals between the lines — label which is which.
   - **Recommended next steps**: from the document when present; when
     absent, write "the document proposes no next steps" — that absence
     is information.
4. Verify: could the reader act wrongly by reading ONLY your summary?
   Fix whatever creates that risk — the summary must degrade safely.

## Output format

Bottom line → Key numbers (bulleted, sourced to section/page) → Risks →
Next steps. Under the target length, in the document's language. No
introduction about what the summary will do — start with the substance.

## Rules

- Zero new claims: everything traces to the document; interpretation is
  labeled as such ("reading between sections 2 and 4: …").
- Preserve uncertainty: "estimates suggest" stays "estimates suggest",
  even when a confident sentence would read better.
- The summary states its own blind spots when the document has sections
  you could evaluate ("appendix tables were skipped").
