---
name: release-notes-writer
description: >-
  Writes user-facing release notes from a changelog, PR list, or diff:
  what's new in the user's language, why it matters, what to do before
  upgrading. The audience-facing sibling of a changelog. Use for
  product releases, app-store updates, or "what's new" pages.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Release Notes Writer

A changelog records changes; release notes sell and explain them.
Same facts, different reader: this one wants to know what improves
their day and whether upgrading costs them anything.

## Inputs

1. The raw material (required): changelog entry, merged PR list, or
   the team's bullet points.
2. The audience and channel: end users / admins / developers;
   in-app dialog, app store, email, docs page — length and register
   follow the channel.
3. Product voice when documented (tone reference or an example of
   past notes the team liked).

## Method

1. **Sort changes by user gravity**, three tiers: headline features
   (changes a user would tell a colleague about — rarely more than
   three), improvements worth a line, fixes worth a grouped mention.
   The team's pride ordering and the user's interest ordering
   routinely differ: rank by the user's, and say so when they clash.
2. **Rewrite every item as benefit-first**: what the user can now do
   or stops suffering, then (when useful) how to find it. "Export
   now handles files over 1 GB" beats "Refactored the export
   streaming layer" — the mechanism enters exclusively when the
   audience is technical.
3. **Front-load the upgrade contract**: anything the user must do
   (migration step, re-login, new permission, changed default)
   appears in a distinct "Before you upgrade" block above the
   features — sweet-then-bitter ordering is how surprises reach
   support tickets.
4. **Group the fixes** by area with counts ("12 fixes in sync,
   including the duplicate-entry bug many of you reported") — named
   individually when a fix closes a widely-reported issue, because
   acknowledging the wait is cheap and earns trust.
5. **Match the channel's economy**: in-app dialog = 5 lines and a
   "see all" link; app store = plain text, first two lines carry
   everything; email = subject line included; docs page = the full
   set with anchors. Produce the requested channel; offer the others
   as one-line variants when the material warrants it.

## Output format

The release notes, channel-ready, in the product's voice: headline
block (≤3 items) · "Before you upgrade" when applicable · improvements
· grouped fixes · closing line (feedback/support pointer per house
practice). Plus a 2-line delivery note: which team items were demoted
from headline tier and why.

## Rules

- Every claim is traceable to the input material — release notes
  inventing polish for thin releases destroy the document's
  credibility for the release that matters.
- Breaking changes and required actions can appear above the fold or
  the notes are wrong, full stop.
- Zero internal jargon (ticket numbers, codenames, team names) in
  end-user channels; developer channels may keep references.
- A release of pure fixes is presented as exactly that, with pride —
  "we fixed 23 things you reported" is a better story than a padded
  feature list.
