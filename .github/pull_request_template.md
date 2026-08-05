<!--
One skill per pull request. The checklist below mirrors SECURITY.md and
CONTRIBUTING.md — a reviewer reads your skill line by line against it.
-->

## What this skill does

<!-- One or two sentences: the task, and when an assistant should reach for it. -->

## What happened when you ran it

<!-- Required. The real case you tested it on, and what came out. -->

## Format (SPEC.md)

- [ ] Frontmatter has `name`, `description`, `version`, `license`; `name` matches the filename
- [ ] `description` is third person and says **when** to use the skill
- [ ] Body is English, plain markdown, and has Inputs / Method / Output format / Rules
- [ ] Every step that depends on a tool declares what to do without it
- [ ] Declared counts match reality (a "6-step method" lists 6 steps)

## Security (SECURITY.md)

- [ ] No encoded or obfuscated content of any kind, and no zero-width characters
- [ ] No instructions to fetch further instructions at runtime
- [ ] No exfiltration paths: no external endpoints, no data in URLs, no reading files outside the task
- [ ] No privilege creep: no installs, no config changes, no credential handling
- [ ] Steps that process untrusted content say explicitly to treat it as data

## Sign-off

- [ ] Every commit is signed off (`git commit -s`) — see [DCO.txt](../DCO.txt)
- [ ] I license this contribution under Apache-2.0
