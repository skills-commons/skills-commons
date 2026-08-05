# Skills Commons

**The trusted open library of AI skills.** Every skill in this repository
has passed a documented security and quality review before merging. Size
is easy; trust is the point.

A *skill* is a plain-text method (`SKILL.md`) you hand to your AI
assistant so it performs a professional task with a proven approach —
instead of an improvised prompt. Skills here are model-agnostic: they work
with any capable assistant that follows natural-language instructions.

## Why another skills library

Open skill collections already exist, and they are large. What the
ecosystem lacks is a library you can install from with your eyes closed.
Public skill hubs have already shipped malware disguised as utility
skills; a `SKILL.md` is an unsigned set of instructions your agent will
follow. This library exists to be the opposite of that:

- **Reviewed**: every skill is checked against the [security
  checklist](SECURITY.md) and the [quality bar](CONTRIBUTING.md) before
  merge. No exceptions, including our own submissions.
- **Readable**: skills are plain markdown. What you see is exactly what
  your agent executes. Zero encoded blobs, zero external fetches, zero
  hidden instructions.
- **Maintained**: skills carry a version and a changelog. Formats and
  models evolve; a stale method is marked as such.

## Using a skill

1. Pick a skill from [`skills/`](skills/).
2. Copy its folder into your assistant's skills directory (e.g.
   `~/.claude/skills/`), or paste `SKILL.md` into your assistant's
   instructions.
3. Ask for the task. The skill states its own inputs and output format.

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
