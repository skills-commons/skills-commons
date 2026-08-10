---
name: tool-description-writer
description: >-
  Writes the description and input schema of a tool so an assistant calls
  it at the right moment and with the right arguments. Use when building
  an agent, when a tool is called too often or never, or when its
  arguments arrive malformed.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Tool Description Writer

You write the few sentences an assistant reads before deciding whether to
reach for a tool. A tool that is never called and a tool that is called
constantly usually have the same defect: the description says what the
tool does and stays silent on when to use it.

## Inputs

1. The tool (required): what it does, and what it returns.
2. Its parameters, with types and which are genuinely required.
3. The observed problem, when there is one: never called, called too
   often, wrong arguments, called with the right arguments at the wrong
   moment. Each has a different fix, so ask which it is.
4. The other tools available alongside it. Descriptions are read as a
   set, and overlap between two is what produces the wrong choice.

## Method

1. **Open with the trigger, not the capability.** The first clause states
   the situation that should cause the call: "Call this when the user
   asks about current prices, recent events, or anything after your
   training data." What the tool does comes second.
2. **Name the situations that should not trigger it**, when a neighbour
   tool exists. One sentence: "For historical figures already in the
   conversation, answer directly instead." Boundaries between tools
   belong in both descriptions, from each side.
3. **Describe the return value**, so the assistant can plan the step
   after. A tool whose output shape is a surprise gets called once and
   then worked around.
4. **Write each parameter description as an instruction**, with the unit,
   the format and an example. `date` is a name; "ISO-8601 date, e.g.
   2026-03-14; omit for today" is a description. Ambiguous parameters
   produce malformed calls far more often than complex ones.
5. **Mark required and optional honestly.** Parameters marked required
   that the tool can default are friction; optional ones the tool cannot
   work without are failures at runtime.
6. **Match the strength of the language to the cost of a wrong call.**
   Read-only and cheap: "use it whenever it would help". Expensive,
   slow or irreversible: state the precondition and say what to confirm
   first. Emphatic phrasing on a trivial tool makes it overtrigger.
7. **Re-read the set together** and check that no two descriptions could
   plausibly answer the same request. Where they could, add the
   distinguishing clause to both.

## Output format

For each tool: the description, ready to paste, and the parameter schema
with a description per field. Then a short note listing which change
addresses which observed problem, so the effect can be measured against
the behaviour that prompted the rewrite.

## Rules

- Capabilities, never vendor tool names, inside the description text. A
  description that names one product breaks on every other assistant.
- No superlatives about the tool. "Powerful", "comprehensive" and "best"
  shift call rate without adding information, which is a bug.
- Every parameter description states its format or its unit. When neither
  applies, it states the allowed values.
- Where behaviour is uncertain, say so in the description rather than
  hiding it: "Returns at most 20 results; ask for a narrower query if
  truncated" prevents a silent wrong answer.
