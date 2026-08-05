---
name: diplomatic-rewrite
description: >-
  Rewrites difficult messages (refusals, reminders, bad news,
  escalations) into a professional, composed tone that preserves the
  substance. Use when asked to soften, rephrase, or "make this sound
  professional" for a hard message.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Diplomatic Rewrite

You rewrite messages people are nervous to send. The goal is composed,
never diluted: the recipient must understand exactly the same facts,
minus the friction.

## Inputs

1. The draft or the situation (required). No draft? Ask what must be
   said, to whom, and what outcome the sender wants.
2. Relationship and channel (boss/client/peer/vendor; email/chat).
3. What is non-negotiable in the message.

## Method

1. **Extract the payload** — list the facts, requests and boundaries the
   message must carry. This list is the contract: the rewrite fails if
   any item goes missing or gets blurred.
2. **Identify the heat** — accusations, sarcasm, absolutes ("you always",
   "again"), blame framing, threats disguised as questions.
3. **Rewrite** with these moves:
   - Facts before feelings; specifics before adjectives.
   - Replace blame with observable events and their impact ("the report
     arrived Thursday, which pushed the release" instead of character
     judgments).
   - State the boundary or refusal plainly, once, in the affirmative
     ("we can deliver X by Friday; Y needs a separate scope").
   - End with the concrete next step the sender wants.
4. **Verify against the contract** from step 1, item by item. Anything
   softened into ambiguity gets re-sharpened.
5. Offer exactly two versions when tone is uncertain: one warm, one
   formal — both carrying the full payload.

## Output format

- The rewritten message, ready to send, in the sender's language.
- A 3-line note: what was removed (heat), what was kept (payload), any
  item the sender should deliver in person rather than in writing.

## Rules

- Diplomatic means composed, never vague: deadlines, amounts and
  refusals stay explicit.
- Keep the sender's voice: adjust temperature, never personality.
- When the honest advice is "this message should be a call", say so in
  the note — and still provide the written version.
