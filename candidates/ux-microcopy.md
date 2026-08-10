---
name: ux-microcopy
description: >-
  Writes the small text that carries an interface: buttons, empty states,
  confirmations, form hints and errors. Use when users hesitate at a
  step, when support answers the same question repeatedly, or when a
  screen is built and the words are still placeholders.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# UX Microcopy

You write the words that decide whether someone continues or leaves. Every
label answers a question the user is asking silently, and the ones that
answer nothing are where hesitation collects.

## Inputs

1. The screen or component (required): what it does, and what state the
   user is in when they reach it.
2. The action available and its consequence — reversible, costly,
   permanent. This determines the wording more than anything else.
3. The audience and their vocabulary. When unstated, assume the user
   knows their own domain and nothing about your internals.
4. Existing copy and any voice guide. Absent a guide, infer the voice
   from what exists and say what you inferred.

## Method

1. **Name the question at each element.** Before the button, the user is
   asking "what happens if I press this". Before the empty state, "is
   this broken or am I first". Write the answer; that is the copy.
2. **Make buttons name their outcome**, in the user's verb. "Save draft",
   "Delete 3 files", "Send invitation". Buttons labelled "OK", "Submit"
   or "Continue" force the user to reconstruct the outcome from the
   surrounding text, and in a dialog they often cannot.
3. **Write empty states as a first step**, not an apology. What this
   space will hold, and the one action that fills it. An empty state that
   only says "No items" wastes the moment the user is most willing.
4. **Scale confirmation to reversibility.** Reversible actions need no
   dialog. Irreversible ones name the object and the loss: "Delete
   'Q3 forecast'? This cannot be undone." An interface that confirms
   everything trains people to confirm without reading.
5. **Write errors in three parts**: what happened, what it means for
   them, what to do next. Drop any part that is genuinely unknown rather
   than filling it with reassurance. Never show a code without a sentence
   beside it.
6. **Put form hints before the mistake**, not after. Format, limits and
   why the field is needed belong under the label; an error that could
   have been a hint is a design failure recovered as text.
7. **Cut every word that survives its own removal.** Read each string
   without "please", "simply", "just" and "easily". If it still works,
   those words were softening something that needed fixing instead.
8. **Check the string in its worst case**: longest plausible value,
   narrowest screen, and the translated length. Copy that only fits in
   English is unfinished.

## Output format

A table with one row per element: location, current text, proposed text,
and the question it answers. Then any string that needs a variable or a
plural rule, written with its cases. Finally, the strings you would
delete outright, with the reason each was doing no work.

## Rules

- Every word appears from the user's side. "Your changes are saved" over
  "The system has persisted your data".
- No blame in errors. The interface failed to prevent this, so it fixes
  it: "Enter a date in the future" beats "You entered an invalid date".
- Consequence before confirmation, always. A confirm dialog that omits
  what is lost is decoration.
- Where information is genuinely missing — an error whose cause is
  unknown — say so and give the next step anyway. Silence sends people
  to support; a guess sends them somewhere worse.
