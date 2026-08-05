---
name: dependency-update-brief
description: >-
  Turns a dependency update (or a Dependabot/Renovate PR) into a risk
  brief: what actually changed between the versions, breaking-change
  exposure in THIS codebase, and the merge/hold recommendation with its
  test focus. Use before merging version bumps, especially majors.
version: "1.0.0"
license: Apache-2.0
authors: [AGORÀ Intelligence]
---

# Dependency Update Brief

Version bumps are merged on green CI and regretted in production. You
read the release notes so the team can merge with eyes open — and you
measure risk against this codebase's actual usage, never against the
changelog alone.

## Inputs

1. The update (required): package, from-version → to-version, or the
   bot PR containing them.
2. Access to the release notes / changelog / diff between the
   versions (live web when available; otherwise what is provided —
   and findings from memory are labeled as such with a verify flag).
3. The codebase, or at minimum: how the package is used (imports,
   call sites, config), and the lockfile for transitive context.

## Method

1. **Classify the jump**: patch / minor / major per semver, plus the
   honest caveat where the ecosystem's semver discipline is known to
   be loose. Multiple majors skipped = the brief covers EVERY major
   boundary crossed, each with its own breaking set — the middle
   major nobody read is where upgrades die.
2. **Extract the change surface** from release notes and diff:
   breaking changes, deprecations activated, behavior changes
   (defaults flipped, error types changed, timezone/encoding
   handling), security fixes (with CVE when named), new peer/engine
   requirements.
3. **Map against actual usage**: for each breaking or behavioral
   change, grep-level check — does this codebase touch that API,
   that config, that default? Three buckets: **exposed** (call sites
   listed), **possibly exposed** (dynamic usage, needs a human eye —
   say where), **untouched**. An update whose breaking changes all
   land in "untouched" is a different decision than one with two
   exposed sites.
4. **Check the transitive layer**: peer-dependency conflicts, engine
   requirements vs the project's runtime, duplicated versions after
   the bump (lockfile), and the security posture the update fixes —
   a bump that closes a known vulnerability shifts the
   recommendation's default toward merge.
5. **Recommend, with teeth**: MERGE (low surface, tests cover it) /
   MERGE WITH FOCUS (list the 2–5 test scenarios to run first, one
   per exposed site) / HOLD (blocker named, prerequisite work
   listed) / SPLIT (when bundled bumps deserve separate decisions).
   Always state the rollback cost (lockfile revert vs migration
   applied).

## Output format

**Header**: package, jump, semver class, security relevance ·
**Change surface**: breaking / behavioral / deprecations, each
one-lined · **Exposure map**: exposed (with file:line), possibly
exposed, untouched · **Transitive notes** · **Recommendation** with
test focus and rollback cost · **Sources**: which release notes were
actually read (URLs), which claims are from memory (flagged).

## Rules

- The brief distinguishes read-the-notes findings from
  recalled-from-memory claims — a wrong memory about a breaking
  change is worse than a gap, and gets flagged for verification.
- Exposure claims cite file:line or say "grep for X" — an exposure
  map the reader can spot-check is the product.
- Security fixes are surfaced in the header, never buried: holding a
  CVE fix is a decision the brief forces into the open.
- Bundled bot PRs (12 packages, one PR) get the SPLIT treatment by
  default when any single package is major.
