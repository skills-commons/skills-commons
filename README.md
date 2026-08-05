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
Public skill hubs have already shipped malware disguised as utility
skills; a skill file is an unsigned set of instructions your agent will
follow. This library exists to be the opposite of that:

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

**22 skills**, every one merged through the same two-review gate.

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

## Contributing

Contributions are welcome and reviewed seriously — read
[CONTRIBUTING.md](CONTRIBUTING.md) first. The review is the product: a
merge here means someone checked your skill line by line.

## Provenance

Seeded and maintained by [AGORÀ Intelligence](https://agora-intelligence.com),
the team running an autonomous newsroom in production (200+ sourced
articles, three languages, a weekly print magazine). The seed skills are
methods we use in real operations, and every merge is reviewed by a
member of the AGORÀ team. Certified, audited builds and enterprise
variants live on the [AGORÀ Skills catalog](https://agora-intelligence.com/en/skills/);
this library is and stays free.

## License

[Apache-2.0](LICENSE). Use the skills anywhere, including commercially;
keep the notice.
