# Security policy

A skill is a set of instructions an AI agent will follow with the user's
permissions. That makes this repository a supply chain, and we treat it
like one.

## The review every skill passes before merge

Reviewers check, line by line:

1. **No hidden instructions** — no encoded content (base64, hex, unicode
   tricks, zero-width characters), no instructions disguised as examples
   or comments, no language telling the agent to conceal actions from the
   user.
2. **No exfiltration paths** — the skill never instructs the agent to
   send data to external endpoints, embed data in URLs, or read files
   outside the task's scope (credentials, keys, browser profiles, `.env`).
3. **No privilege creep** — no instructions to install software, modify
   system configuration, disable safety measures, or acquire credentials.
4. **No remote loading** — the skill is complete as written; it never
   fetches additional instructions at runtime.
5. **Prompt-injection surface** — steps that process untrusted content
   (web pages, emails, documents) must treat that content as data, and
   say so explicitly.
6. **Self-consistency** — declared counts, referenced sections and output
   formats match the actual text (drift hides tampering).

Merges require an approving review from a maintainer. Maintainer
submissions get reviewed by a different maintainer.

## Reporting a vulnerability

Found a malicious pattern, an injection vector, or a dangerous
instruction in a merged skill? Open a private report on GitHub (Security tab, "Report a vulnerability") or email **hello@agora-intelligence.com** with subject `[skills-commons security]`. We acknowledge within 72 hours. Confirmed
reports lead to immediate skill removal, a public advisory in the skill's
folder, and credit to the reporter (with consent).

## Scope

This policy covers the skills and documents in this repository. Forks,
mirrors and downstream copies are outside our control: verify you are
installing from this repository and review the diff of any update.
