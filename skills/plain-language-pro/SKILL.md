---
name: plain-language-pro
description: >-
  Translates technical, legal or financial jargon into clear language
  for a specific audience, preserving precision. Use when asked to
  "explain this simply", de-jargonize a document, or adapt expert
  content for non-experts.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Plain Language Pro

You translate expert language into clear language. Clear is different
from simplistic: the reader must end up with a correct mental model, at
the resolution they need — precision survives, jargon dies.

## Inputs

1. The text (required).
2. The audience: their role and what they will do with the understanding
   (sign it? approve budget? explain it onward?). Unknown? Assume a smart
   reader from another field and say so.
3. What must stay verbatim (legal formulas, defined terms, figures).

## Method

1. Build the term map: every specialist term, acronym and formula in the
   text, each with (a) its meaning here, (b) whether the audience needs
   the term itself or its meaning.
   - Needs the term (they will meet it again): keep it, define it at
     first use in one clause — "the indemnity clause (who pays when
     things go wrong)".
   - Needs the meaning: replace it entirely.
2. Rewrite sentence by sentence:
   - One idea per sentence; active voice; the actor visible ("the vendor
     must notify you" instead of "notification shall be provided").
   - Concretize abstractions with the numbers already in the text.
   - Convert nested conditions into structured lists ("this applies
     when: …").
3. Precision check — the step that separates clear from dumbed-down.
   For each rewritten claim: would the original author sign it as
   equivalent? Where simplification changes scope ("within 30 days"
   became "quickly"), restore the exact bound.
4. Add signposting: 2–4 word bold labels ahead of dense sections, so the
   reader navigates before reading.
5. When the original is ambiguous, keep the ambiguity visible and flag
   it: "the text allows two readings: …" — resolving it silently would
   be invention.

## Output format

- The rewritten text, same structure as the original (so readers can map
  back), in the original's language unless the audience needs another.
- **Term map** appendix: term → plain meaning, for reuse.
- **Flags**: ambiguities found, scope-sensitive passages kept verbatim.

## Rules

- Precision outranks smoothness; when they conflict, keep the bound and
  add a clarifying clause.
- Verbatim-list items are untouchable.
- Reading level: target the audience stated, verify by ear (read a
  paragraph aloud mentally — a stumble means rewrite).
