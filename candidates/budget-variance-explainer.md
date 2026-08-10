---
name: budget-variance-explainer
description: >-
  Explains why actuals differ from budget and what the difference forces
  someone to decide. Use for monthly or quarterly reviews, board packs,
  or any variance report that currently lists numbers without saying
  what they mean.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Budget Variance Explainer

You turn a table of differences into a short account of what changed and
what it now costs to ignore. A variance report that ends at the numbers
leaves the reader to invent the causes, and they will.

## Inputs

1. The figures (required): budget and actual per line, for the period.
   State the period and the currency you were given.
2. The prior period's actuals, when available — a variance that repeats
   is a different problem from one that appears once.
3. Known events: a delayed hire, a renegotiated contract, a campaign
   moved. Absent these, the explanation stays at the level of "what",
   and you say so rather than inferring a cause.
4. The materiality threshold. When unstated, use 5% or the largest ten
   lines, whichever is fewer, and declare the rule you applied.

## Method

1. **Sort by absolute variance, not by line order.** The reader has time
   for the largest handful; the chart of accounts order buries them.
2. **Separate timing from spend.** An invoice that arrived late is not
   an overspend, and treating it as one produces a decision that
   reverses itself next month. Label each variance as timing,
   volume, price, or scope.
3. **Say what each material variance is**, in one sentence, in the units
   of the business rather than of the ledger: "Cloud spend is 18% over
   because the migration ran in parallel with the old cluster for six
   weeks."
4. **Attribute only what the inputs support.** Where the cause is
   unknown, write "cause not established" and name who would know. An
   invented explanation is the most durable error in this document.
5. **Net the offsetting variances explicitly.** An underspend covering an
   overspend is a coincidence, not a plan, and reporting only the net
   hides two facts that each need a decision.
6. **Project the run rate**: if this variance continues, what is the
   full-year effect. This converts a historical table into something
   actionable, and it is the number the reader actually wants.
7. **End with the decisions**, at most three: what needs approving,
   stopping or reforecasting, each with the number attached.

## Output format

Headline in two lines — total variance and its direction, and the single
largest driver. Then a table of material variances with amount, percent,
type (timing, volume, price, scope) and a one-line cause. Then the run
rate implication, and the decisions required with their owners. Anything
immaterial is summarised in one line as immaterial, with the threshold
stated.

## Rules

- Every cause is either sourced from the inputs or marked as not
  established. Plausible causes written as fact are the failure mode this
  skill exists to prevent.
- Timing differences are never described as savings or overspends.
- Percentages always carry the absolute figure beside them; 40% of a
  small line has misled many boards.
- The reconciliation holds: the material variances plus the immaterial
  remainder equal the total. State that total so a reader can check.
