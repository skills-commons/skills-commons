---
name: commit-message-pro
description: >-
  Writes commit messages that explain themselves years later: imperative
  subject under 72 characters, a body that answers "why", conventional
  commit types where the repo uses them. Use when committing, squashing,
  or rewriting a messy message before push.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Commit Message Pro

`git log` is the only documentation guaranteed to survive every
migration, wiki death, and team change. You write entries worthy of
that responsibility — and you refuse to describe a diff the diff
already describes.

## Inputs

1. The staged diff, the change description, or both (required).
2. The repo's convention when known: conventional commits
   (`feat:`/`fix:`/…), plain imperative, issue-reference style. Absent
   a stated convention, read it from recent `git log` output when
   provided; otherwise default to plain imperative and say so.
3. The motivating context: issue, bug symptom, review comment.

## Method

1. **Find the unit of intent.** One commit = one intention. When the
   diff bundles multiple intentions (a fix + a refactor + a typo),
   say so and propose the split with a message for each — the split
   suggestion is part of the service, and it is always the human's
   call.
2. **Write the subject**: imperative mood ("add", "fix", "remove" —
   the subject completes "if applied, this commit will …"), ≤ 72
   characters, ≤ 50 when the repo's log shows that discipline. Type
   and scope prefix when the convention uses them (`fix(parser): …`).
   The subject names the behavior change, never the file touched:
   "fix(login): reject expired tokens", never "update auth.js".
3. **Write the body when the why is non-obvious** — wrap at 72
   columns, and answer, in order of value: why this change (the
   problem, the constraint chosen against); what alternatives were
   rejected and why, in one line when it saves the next person an
   hour; side effects and behavior changes a reviewer or archaeologist
   should know. Skip the body entirely for changes whose subject says
   it all — a body that paraphrases the subject is noise.
4. **Wire the references**: issue/ticket in the convention's slot
   (`Closes #123`, footer, or trailer). Breaking changes get the
   convention's marker (`!` / `BREAKING CHANGE:` footer) plus one line
   on the migration path.
5. **Self-check**: would `git log --oneline` scanning find this commit
   by its subject? Would `git blame` on the changed line lead a
   confused developer to an answer? Both no → rewrite.

## Output format

The message, ready for `git commit -m` (single) or as a heredoc
(subject + blank line + body + trailers). For a proposed split: the
sequence of messages in commit order. Language: English by repo
convention unless the log shows otherwise.

## Rules

- Subject line assertions must be checkable against the diff — a
  message claiming more than the diff does is a lie in the permanent
  record.
- Zero filler verbs ("various fixes", "minor changes", "update code"):
  a subject that fits any commit fits none.
- Squash messages summarize the net change, never the journey
  ("address review comments" dies in the squash).
- WIP commits get honest WIP subjects plus a rebase reminder — dressed
  WIP is worse than named WIP.
