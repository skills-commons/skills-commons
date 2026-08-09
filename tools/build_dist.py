#!/usr/bin/env python3
"""Build the installable, spec-conformant tree from the flat library.

The library stores one file per skill — `skills/<category>/<name>.md` — because
that keeps diffs readable and review honest. The Agent Skills specification
(https://agentskills.io/specification) instead defines a skill as a *directory*
containing `SKILL.md`, with `name` matching the parent directory.

This script produces that shape, so a user installs a skill by copying one
folder instead of creating it by hand:

    dist/<category>/<name>/SKILL.md

Frontmatter is normalised to the spec while it goes: `name`, `description` and
`license` stay top level; `version` and `authors` move under `metadata`, which
is where the spec puts fields it does not define itself.

  python tools/build_dist.py            # build into dist/
  python tools/build_dist.py --check    # verify only, write nothing
"""

from __future__ import annotations

import glob
import os
import shutil
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

SPEC_TOP_LEVEL = ["name", "description", "license", "compatibility", "allowed-tools"]
OUT = "dist"


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[3:end], text[end + 4 :]


def to_spec(data: dict) -> dict:
    """Reshape house frontmatter into the specification's field set."""
    out: dict = {}
    for key in SPEC_TOP_LEVEL:
        if data.get(key) not in (None, ""):
            out[key] = data[key]

    metadata: dict[str, str] = {}
    for key, value in data.items():
        if key in SPEC_TOP_LEVEL:
            continue
        # metadata is "a map from string keys to string values" per the spec.
        if isinstance(value, (list, tuple)):
            value = ", ".join(str(v) for v in value)
        metadata[str(key)] = str(value)
    if metadata:
        out["metadata"] = metadata
    return out


def build(check_only: bool = False) -> int:
    sources = sorted(glob.glob("skills/*/*.md"))
    if not sources:
        print("No skills found under skills/*/*.md")
        return 1

    if not check_only and os.path.isdir(OUT):
        shutil.rmtree(OUT)

    problems: list[str] = []
    built = 0

    for src in sources:
        norm = src.replace("\\", "/")
        category = norm.split("/")[1]
        stem = os.path.basename(norm)[:-3]

        text = open(src, encoding="utf-8").read()
        fm, body = split_frontmatter(text)
        if fm is None:
            problems.append(f"{norm}: no frontmatter")
            continue
        try:
            data = yaml.safe_load(fm)
        except yaml.YAMLError as exc:
            problems.append(f"{norm}: invalid YAML — {str(exc).splitlines()[0]}")
            continue
        if not isinstance(data, dict):
            problems.append(f"{norm}: frontmatter is not a mapping")
            continue

        spec = to_spec(data)
        name = spec.get("name")

        # The spec's own rule: name must match the parent directory it lands in.
        if name != stem:
            problems.append(f"{norm}: name '{name}' would land in a directory named '{stem}'")
            continue

        rendered = (
            "---\n"
            + yaml.safe_dump(spec, sort_keys=False, allow_unicode=True, width=88).rstrip("\n")
            + "\n---\n"
            + body.lstrip("\n")
        )

        # Round-trip: the artefact we ship must parse back to what we meant.
        again, _ = split_frontmatter(rendered)
        parsed = yaml.safe_load(again)
        if parsed != spec:
            problems.append(f"{norm}: frontmatter does not survive a round trip")
            continue

        if not check_only:
            target = os.path.join(OUT, category, stem)
            os.makedirs(target, exist_ok=True)
            with open(os.path.join(target, "SKILL.md"), "w", encoding="utf-8", newline="\n") as fh:
                fh.write(rendered)
        built += 1

    verb = "would build" if check_only else "built"
    print(f"{verb} {built} skill(s) into {OUT}/<category>/<name>/SKILL.md")
    for p in problems:
        print(f"  error: {p}")
    if problems:
        print(f"{len(problems)} problem(s).")
        return 1
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(build("--check" in sys.argv))
