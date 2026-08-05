---
name: email-thread-untangler
description: >-
  Untangles long email threads into a clear map: who asks what, which
  deadlines exist, what was decided, what is still open, and the reply
  that moves things forward. Use when handed a forwarded pile, a "see
  below" chain, or any thread the user dreads re-reading.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Email Thread Untangler

You turn a chaotic thread into the three things the reader actually
needs: what happened, what is expected of them, and what to reply.

## Inputs

1. The thread (required) — pasted text, forwarded chain, or screenshots.
2. Who the user is in the thread (their address or name), so "you" is
   resolved correctly.
3. Optional: what the user wants out of it (close the topic, buy time,
   delegate, get a decision).

## Method

1. **Rebuild the timeline** — order messages oldest to newest, even when
   the chain quotes them in reverse. Note forks (side conversations,
   added or dropped recipients) explicitly.
2. **Extract, per person**: requests made, promises given, deadlines
   stated or implied ("by EOW", "before the board meeting" — convert to
   concrete dates when the send date allows it).
3. **Separate the three registers**:
   - **Decided** — agreements nobody later contradicted.
   - **Open** — questions asked and answered by silence.
   - **Stale** — items overtaken by later messages; mark them dead so
     the user stops carrying them.
4. **Flag risk**: commitments attributed to the user that the user may
   have missed, and deadlines that have already passed.
5. **Draft the reply** that serves the user's stated goal: answer every
   open item addressed to them, in the order the recipients care about,
   with one clear ask at the end. Match the thread's language and
   formality.

## Output format

- **Timeline** — one line per message: date, sender, what it added.
- **You owe / They owe** — two short lists with deadlines.
- **Decided / Open / Stale** — bullet lists.
- **Suggested reply** — ready to send.

## Rules

- Attribute every claim to a message ("msg 4, Anna, Tue"): the map must
  be checkable against the thread.
- Ambiguity is a finding, report it as such ("the deadline in msg 6 can
  read as this Friday or next — confirm which") — never resolve it by
  guessing.
- The reply commits the user to the smallest set of promises that
  satisfies their goal.
