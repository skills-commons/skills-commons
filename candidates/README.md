# Candidates

Skills proposed for the library that **no one has read yet**.

Nothing in this folder is part of the library. It is not in the release, it is
not in `dist/`, and the guarantees on
[skills-commons.org](https://skills-commons.org) do not apply to it. A file
here has passed the automated checks and nothing more.

## Why this folder exists

The library grows by writing more skills. The claim that gives the library its
value is that a person read each one line by line before it merged. Those two
facts pull against each other, and the honest way to hold both is to separate
the queue from the shelf:

- `candidates/` — proposed, machine-checked, unread. Public, so the pipeline
  is visible rather than hidden.
- `skills/` — read line by line, merged, covered by every claim we make.

A skill moves from the first to the second when someone has actually read it.
It never moves the other way, and volume in here never becomes a number we
quote as if it were the library.

## How a candidate is promoted

1. It passes `python tools/skill_lint.py` with zero errors.
2. Someone runs it on a real case and pastes the output in the pull request —
   a method that has never been executed is a guess with formatting.
3. A maintainer reads it against [SECURITY.md](../SECURITY.md) and the quality
   bar in [CONTRIBUTING.md](../CONTRIBUTING.md).
4. It moves to `skills/<category>/<name>.md` in that pull request, and the
   candidate file is deleted in the same commit.

Step 2 is the one that catches what neither automation nor a careful read
will: a method that looks rigorous and produces nothing useful.

## Rejecting is normal

A candidate that survives review unchanged is the exception. Most need the
vague step made decidable, the missing degradation clause written, or the
output contract that was never specified. Some are deleted, and that is the
folder working as intended.

## Status

See [TOPICS.md](TOPICS.md) for the queue and what has been drafted so far.
