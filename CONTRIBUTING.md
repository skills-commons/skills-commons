# Contributing

A merge here means a human checked your skill line by line. That review is
what makes this library worth installing from — thank you for going
through it.

## What belongs here

Professional methods for AI assistants: tasks people re-explain to their
AI every day, packaged once, well. Generic craft only — no skills that
require or reveal proprietary systems, no vendor-specific hacks, no
content that needs credentials to demonstrate.

## How to submit

1. Read [SPEC.md](SPEC.md) and mirror an existing skill's structure.
2. One skill per pull request, as `skills/<category>/<your-skill-name>.md` (categories: workplace, writing, engineering, agents — propose a new one in the PR when yours fits none).
3. Fill the PR template checklist (it mirrors [SECURITY.md](SECURITY.md)).
4. Expect real review: questions about ambiguous steps, requests to count
   your own checklist, pushback on vague verbs. The automated checks must
   pass, and then a maintainer reads the file line by line. Both happen in
   the pull request, where anyone can see how deep the reading went.

## The quality bar

- **Executable, honestly**: an assistant with common tools can follow
  every step; steps that need special tools declare their fallback.
- **Direct**: no motivational filler, no repeated framing. Every sentence
  either instructs or constrains.
- **Self-consistent**: declared counts match actual items; the output
  format section matches what the method produces.
- **Tested**: you ran it at least once on a real case and the PR
  description says what happened.

## Check the structure before you open the PR

```
pip install pyyaml
python tools/skill_lint.py
```

It checks what can be checked mechanically: frontmatter, the required
sections, `name` against the filename, counts that contradict themselves,
invisible characters, encoded blobs. It runs on every pull request and
reports inline.

What it deliberately does not do is judge your method. Whether a step is
decidable, whether the description states a usable trigger, whether the
skill says what to do when it cannot know — those are read by a human,
because a keyword count gets them wrong. An all-clear here means the file
is well-formed, nothing more.

## Sign your commits (DCO)

Every commit needs a `Signed-off-by` line. Add it automatically:

```
git commit -s -m "Add my-skill"
```

which appends:

```
Signed-off-by: Your Name <your@email.com>
```

That line is the [Developer Certificate of Origin](DCO.txt): you certify
you wrote the contribution, or have the right to submit it, and that it
can ship under Apache-2.0. Use your real name and an email you control —
a CI check verifies the sign-off matches the commit author.

Forgot on the last commit? `git commit --amend -s --no-edit`. Forgot on
several? `git rebase --signoff main`. Then `git push --force-with-lease`.

## Credit

Contributors are listed in the skill's frontmatter (`authors:`) and in
release notes. By submitting, you license your contribution under
Apache-2.0.

## Maintainers

Seeded and maintained by AGORÀ Intelligence. Maintainer decisions aim for
the library's trust first; when in doubt, we decline politely and explain
why.
