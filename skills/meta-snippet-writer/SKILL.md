---
name: meta-snippet-writer
description: >-
  Writes title tags, meta descriptions and social preview text that earn
  the click honestly: within pixel limits, matched to search intent,
  free of clickbait debt. Use for new pages, refreshes of
  underperforming snippets, or batches from a URL list.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Meta Snippet Writer

A snippet is a promise the page must keep. You write the promise
precisely: compelling enough to win the click, accurate enough that the
visitor stays.

## Inputs

1. The page: URL, draft, or an honest summary of what it delivers
   (required).
2. The primary query or intent the page targets; secondary terms when
   known.
3. Current title/description and their performance, for refreshes.

## Method

1. **Extract the page's strongest claim** — the most specific, checkable
   value it delivers (a number, a method, a result, a differentiator).
   Generic pages get the honest question back: "what does this page do
   that the top results skip?"
2. **Match intent shape**: informational intent leads with the answer's
   existence, transactional with the offer and its qualifier,
   navigational with the name. The snippet mirrors the words a searcher
   would use, front-loaded.
3. **Write the title**: primary term near the front, claim next, brand
   last when space allows — target ≤ 60 characters (~570px). Every word
   pulls weight; articles and filler go first when trimming.
4. **Write the description**: 140–155 characters, one sentence of claim
   + one of proof or specifics, ending with an implicit reason to click.
   Active voice, present tense, zero ellipsis bait.
5. **Write the social variant** (og:title / og:description): looser
   limits, same honesty; the hook may be warmer since it appears in a
   feed, off the results page.
6. **Self-check**: would the page's own author agree the snippet
   describes it? Would a visitor who clicked feel the promise was kept?
   A "no" on either sends it back to step 1.

## Output format

Per page: Title (with character count) · Meta description (count) ·
og:title / og:description · one-line rationale naming the intent and
the claim used. Batches arrive as a table.

## Rules

- Hard limits enforced: flag any title over 60 or description over 158
  characters with a trimmed alternative.
- The snippet claims what the page proves — a promise the page breaks
  costs rankings through pogo-sticking and costs trust through memory.
- One primary intent per snippet; pages chasing two intents get the
  advice to split.
- Refreshes state what changed and why ("front-loaded the number, cut
  the brand to fit the claim").
