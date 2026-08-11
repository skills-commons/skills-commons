# Skills Commons

**The trusted open library of AI skills.** Every skill in this repository
has passed a documented security and quality review before merging. Size
is easy; trust is the point.

A *skill* is a plain-text method (a single `.md` file) you hand to your AI
assistant so it performs a professional task with a proven approach —
instead of an improvised prompt. Skills here are model-agnostic: they work
with any capable assistant that follows natural-language instructions.

## Why another skills library

Open skill collections already exist, and they are large. What the
ecosystem lacks is a library you can install from with your eyes closed.

The gap is measured. Scanning 3,984 skills across two public hubs on
5 February 2026, [Snyk found](https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/)
that 36.82% carried at least one security flaw and 13.4% at least one
critical issue, alongside 76 payloads built for credential theft,
backdoors and exfiltration. The first systematic security analysis of the
format, [Towards Secure Agent Skills](https://arxiv.org/abs/2604.02837)
(Li, Wu, Ling, Cui and Luo, April 2026), names *the absence of mandatory
marketplace security review* as one of three architectural weaknesses
behind the worst of those threats.

A skill file is an unsigned set of instructions your agent runs with your
permissions. This library exists to be the opposite of that:

- **Reviewed**: every skill is checked against the [security
  checklist](SECURITY.md) and the [quality bar](CONTRIBUTING.md) before
  merge. No exceptions, including our own submissions.
- **Readable**: skills are plain markdown. What you see is exactly what
  your agent executes. Zero encoded blobs, zero external fetches, zero
  hidden instructions.
- **Maintained**: skills carry a version and a changelog. Formats and
  models evolve; a stale method is marked as such.

## The library

One skill = one markdown file, named after itself, in its category:

| Category | Skills |
|---|---|
| [`workplace/`](skills/workplace/) | diplomatic-rewrite · email-thread-untangler · executive-summary-builder · job-description-writer · meeting-minutes-pro · note-organizer-pro |
| [`writing/`](skills/writing/) | meta-snippet-writer · plain-language-pro |
| [`engineering/`](skills/engineering/) | bug-report-pro · changelog-writer · commit-message-pro · dependency-update-brief · issue-triage-pro · pr-description-writer · readme-architect · release-notes-writer · sql-query-reviewer · stack-trace-explainer |
| [`agents/`](skills/agents/) | honest-status-report · session-summary-writer · task-handoff-brief · tool-failure-triage |

**22 skills**, every one read line by line before it merged.

All 22 were written by AGORÀ Intelligence to seed the library. That is a
starting point, not the destination — see below.

## Wanted

**This library is deliberately small, and stays that way.** The ceiling is
around a hundred skills, not thousands. A collection nobody can read through
is a collection nobody checked, and there are already several of those.

So the interesting number here is not what exists. It is what is missing:

### → [100 skills we want and do not have](candidates/TOPICS.md)

Pick one. The list is weighted toward the categories this library is thinnest
in — `writing/` has two skills today against ten in `engineering/` — and each
entry says in one line what the skill should do.

You do not need permission and you do not need to be first. If a topic is
already drafted in [`candidates/`](candidates/), the draft has still not been
read by anyone; a better version replaces it.

**The one number worth watching:** every skill here is currently authored by
the same team. The first skill merged from outside is what turns a company's
open catalogue into a commons, and it is worth more to this project than the
next fifty we write ourselves.

Start with [Write Your First Skill](https://skills-commons.org/write/) —
anatomy, a reviewed example, the mistakes reviews reject, and a browser editor
that generates a conformant file.

## Using a skill

1. Pick a skill from [`skills/`](skills/).
2. Install it in the way your assistant expects:
   - **Claude Code / Claude Desktop**: create a folder named after the
     skill in your skills directory and save the file inside it as
     `SKILL.md` (e.g. `~/.claude/skills/commit-message-pro/SKILL.md`).
   - **Claude.ai / ChatGPT / Gemini projects**: paste the file into the
     project's instructions.
   - **Any assistant**: paste the file as your first message, then ask.
3. Ask for the task. The skill states its own inputs and output format.

Skills are written model-agnostic on purpose: they name capabilities
("when code execution is available"), never one vendor's tool names.

### Or skip the folder-making

The library is stored one file per skill because that keeps diffs
readable and review honest. The [Agent Skills
specification](https://agentskills.io/specification) instead defines a
skill as a *directory* containing `SKILL.md`, with `name` matching that
directory. Both shapes ship:

```
python tools/build_dist.py     # -> dist/<category>/<name>/SKILL.md
```

The built tree is spec-shaped — `version` and `authors` move under
`metadata`, where the spec puts fields it does not define — so installing
is copying one folder. Every push builds it in CI and attaches it as the
`skills-spec-tree` artifact.

## Tools

| Command | What it does |
|---|---|
| `python tools/skill_lint.py` | Structural checks against SPEC.md and SECURITY.md. Runs on every PR. |
| `python tools/skill_lint.py --spec-only` | Only the Agent Skills spec and the safety checks — usable on any skill, ours or not. |
| `python tools/build_dist.py` | Builds the installable, spec-conformant tree. |
| `python tools/compare_corpus.py` | Measures this library against [anthropics/skills](https://github.com/anthropics/skills) on shared ground, and reports the licence each of those skills actually carries. |
| `python tools/review_agent.py` | Reads each candidate three times with three different lenses, scores six axes, and rejects what a person should not spend time on. Never approves. Needs API credentials; `--rubric` and `--dry-run` do not. |
| `python tools/repeatability.py` | Runs each skill several times on a frozen input and measures how much the outputs agree. Needs API credentials; `--self-test` and `--dry-run` do not. |

The first four need only `pyyaml`.

### Repeatability

Structural checks say a file is well-formed. They say nothing about the
question that actually matters to someone installing it: *will this
produce the same work twice?*

`tools/repeatability.py` answers it by measurement. Each skill runs
several times against a frozen input in [`tests/fixtures/`](tests/fixtures/),
and the outputs are compared to each other:

| Number | Reads as |
|---|---|
| `structure` | agreement on the shape — headings, labels, table columns |
| `content` | agreement on the words, over 3-word shingles |
| `length cv` / `items cv` | how much the volume moves between runs |

They stay separate on purpose. High structure with low content is the
interesting case: the deliverable's shape is pinned and its substance is
being improvised — which is exactly where a reader gets a confident
answer that was invented.

**This measures repeatability, not correctness.** A skill can be
consistently wrong and score 1.00. What it does measure is how much of
the work the file decided, and how much it left to the model.

```
python tools/repeatability.py --self-test   # validates the metric, no API
python tools/repeatability.py --dry-run     # shows the plan and the call count
python tools/repeatability.py --runs 3      # measures
```

Results depend on the model and effort used, so both are recorded in the
output alongside the numbers. Server-side fallback is deliberately off:
answering with a substitute model mid-run would make one number describe
two models.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), take a topic from
[the wanted list](candidates/TOPICS.md), and open one pull request per skill.
Two gates, both public in that pull request: the automated checks must pass,
and then a person reads the file line by line. Credit lands in the skill's own
frontmatter and stays there.

Expect the review to argue with you. Vague steps get sent back, missing
degradation clauses get sent back, and a method with no output contract gets
sent back. That is the product working — a merge here means something because
it is possible to fail.

## Provenance

Seeded and maintained by [AGORÀ Intelligence](https://agora-intelligence.com),
the team running an autonomous newsroom in production (200+ sourced
articles, three languages, a weekly print magazine). The seed skills are
methods used in real operations, and every merge is read by a member of the
team.

### What is free, and what is not

Everything AGORÀ writes for this library lands in this library. There is no
tier where the better version is held back — a method good enough to charge
for is a method good enough to prove we can do the work, and proving it is
worth more than the file.

What [AGORÀ](https://agora-intelligence.com/en/skills/) sells is a different
object, not a better copy of this one: a skill built against one company's
data, systems, tone and compliance rules; skills that must stay private;
audits with a name attached; measurement run on your own skills rather than
ours. A method is a text and texts get copied. An implementation is work, and
it has to be done again for every organisation.

That line is the reason this library can stay free without being the leftovers.

## License

[Apache-2.0](LICENSE). Use the skills anywhere, including commercially;
keep the notice.
