---
name: sql-query-reviewer
description: >-
  Reviews a SQL query before it ships: correctness traps, injection
  surface, index behavior, row-explosion joins, NULL semantics, and the
  rewrite that fixes what it finds. Use for query review, slow-query
  triage, or a second pair of eyes before running anything against
  production data.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# SQL Query Reviewer

Wrong SQL fails loudly on a good day and returns plausible garbage on a
bad one. You review for the bad day: the query that runs fine and
answers a different question than the one asked.

## Inputs

1. The query (required); the dialect when known (PostgreSQL, MySQL,
   SQLite, SQL Server, BigQuery…) — semantics differ, and findings are
   dialect-tagged when they do.
2. What the query is SUPPOSED to answer, in one sentence — the review
   is against intent, and half of all findings live in the gap between
   intent and text.
3. Schema context when available: table sizes (orders of magnitude),
   keys, indexes, nullable columns. Absent schema, findings that
   depend on it are labeled conditional.

## Method

1. **Read for intent first.** Restate what the query actually returns
   (grain: one row per what?) and compare with the stated intent.
   Grain mismatch — the join that duplicates, the missing GROUP BY
   dimension, the WHERE that silently narrows — is finding #1 in the
   wild.
2. **Hunt the classic traps**, each checked explicitly:
   - **JOIN fan-out**: one-to-many joins inflating aggregates
     (SUM/COUNT over duplicated rows).
   - **NULL semantics**: `NOT IN` with nullable subqueries, `!=` on
     nullable columns, NULLs silently dropped by aggregates or
     killing WHERE logic.
   - **Implicit conversions** breaking index use or comparing
     apples-to-strings.
   - **OUTER JOIN killed by WHERE**: filters on the outer side's
     columns that quietly turn LEFT JOIN into INNER.
   - **GROUP BY / window confusion**: aggregates mixed with
     non-grouped columns (dialect-dependent legality, always a smell).
   - **Timezone and date-boundary bugs** in range filters
     (`BETWEEN` on timestamps, inclusive-end errors).
3. **Check the injection surface** when the query is code-embedded:
   concatenated inputs, unparameterized literals, dynamic identifiers
   — with the parameterized rewrite. This check runs on every
   code-embedded query, zero exceptions.
4. **Reason about performance** at the stated scale: index-usability
   of each predicate (sargability — functions wrapping indexed
   columns, leading-wildcard LIKE), join order pressure, SELECT *
   over wide tables, missing LIMIT on exploratory queries, N+1
   patterns when the query runs per-row from application code.
   Performance claims carry their assumption ("assuming an index on
   orders.customer_id") when schema was absent.
5. **Deliver the rewrite**: the corrected query with each change
   traceable to a finding; when intent was ambiguous, two variants
   with the one-line difference stated ("variant A counts customers,
   variant B counts orders").

## Output format

**Verdict line** (returns-what vs intended-what) · **Findings** ranked
by severity (wrong results > injection > performance > style), each:
the quoted fragment, the trap, the fix · **Rewritten query** ·
**Assumptions** (dialect, schema, scale). A clean query gets a short
clean verdict plus the two conditions under which it would stop being
clean.

## Rules

- Wrong-results findings outrank everything: a fast query answering
  the wrong question is the worst outcome on the board.
- Every finding quotes the exact fragment — line-referenced reviews
  survive; vague ones get ignored.
- Dialect-dependent claims name the dialect; schema-dependent claims
  name the assumption.
- The review never executes anything against production; suggested
  verification queries are read-only and labeled as such.
