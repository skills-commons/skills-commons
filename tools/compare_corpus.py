#!/usr/bin/env python3
"""Measure this library against an outside corpus on shared ground.

Our own checks say a file follows *our* rules, which is not a number anyone
outside can read. This compares the library with the reference corpus at
https://github.com/anthropics/skills using only the constraints both are
bound by: the Agent Skills specification (https://agentskills.io/specification)
and the safety checks that apply to any skill anywhere. House rules are
switched off on both sides, so the comparison is like for like.

It also reports the licence each outside skill actually carries, read from its
own LICENSE.txt rather than from a summary — which matters before anyone
reuses one.

  python tools/compare_corpus.py                    # clones into a temp dir
  python tools/compare_corpus.py --corpus PATH      # use a local checkout
"""

from __future__ import annotations

import glob
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

from skill_lint import lint  # noqa: E402

CORPUS_URL = "https://github.com/anthropics/skills.git"


def frontmatter(path: str) -> dict:
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def licence_of(skill_dir: str) -> str:
    path = os.path.join(skill_dir, "LICENSE.txt")
    if not os.path.isfile(path):
        return "unstated"
    head = open(path, encoding="utf-8", errors="replace").read(400)
    if re.search(r"Apache License", head):
        return "Apache-2.0"
    if re.search(r"All rights reserved", head, re.I):
        return "source-available"
    return "other"


def measure(files: list[str], label: str) -> dict:
    reports = [lint(f, spec_only=True) for f in files]
    descs = [len(" ".join(str(frontmatter(f).get("description", "")).split())) for f in files]
    findings = sum(len(r.findings) for r in reports)
    return {
        "label": label,
        "n": len(files),
        "errors": sum(len(r.errors) for r in reports),
        "warnings": sum(len(r.warnings) for r in reports),
        "clean": sum(1 for r in reports if not r.findings),
        "median_desc": sorted(descs)[len(descs) // 2] if descs else 0,
        "max_desc": max(descs) if descs else 0,
        "findings": findings,
        "reports": reports,
    }


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    corpus = None
    if "--corpus" in argv:
        corpus = argv[argv.index("--corpus") + 1]
    tmp = None
    if not corpus:
        tmp = tempfile.mkdtemp(prefix="skills-corpus-")
        corpus = os.path.join(tmp, "skills")
        print(f"Cloning {CORPUS_URL} …")
        rc = subprocess.call(["git", "clone", "--depth", "1", "--quiet", CORPUS_URL, corpus])
        if rc != 0:
            print("Clone failed. Pass a local checkout with --corpus PATH.")
            return 1

    ours = sorted(glob.glob("skills/*/*.md"))
    theirs = sorted(glob.glob(os.path.join(corpus, "skills", "*", "SKILL.md")))
    if not ours or not theirs:
        print("Nothing to compare — run from the repository root.")
        return 1

    rev = subprocess.run(
        ["git", "-C", corpus, "log", "-1", "--format=%h %ad", "--date=short"],
        capture_output=True, text=True,
    ).stdout.strip()

    a = measure(ours, "skills-commons")
    b = measure(theirs, f"anthropics/skills @ {rev}")

    print("\nMeasured on the Agent Skills specification and the safety checks only.")
    print("House rules are off on both sides.\n")
    print(f"{'':34} {'skills':>7} {'clean':>7} {'errors':>7} {'warnings':>9} {'median desc':>12}")
    for m in (a, b):
        print(f"{m['label']:34} {m['n']:7} {m['clean']:7} {m['errors']:7} {m['warnings']:9} {m['median_desc']:12}")

    print("\nFindings in the outside corpus:")
    any_found = False
    for r in b["reports"]:
        for level, code, msg, line in r.findings:
            short = os.path.basename(os.path.dirname(r.path))
            print(f"  {short:24} {level:5} {code}  {msg[:74]}")
            any_found = True
    if not any_found:
        print("  none")

    print("\nLicence carried by each outside skill (read from its own LICENSE.txt):")
    buckets: dict[str, list[str]] = {}
    for f in theirs:
        d = os.path.dirname(f)
        buckets.setdefault(licence_of(d), []).append(os.path.basename(d))
    for lic in sorted(buckets):
        names = ", ".join(sorted(buckets[lic]))
        print(f"  {lic:18} {len(buckets[lic]):2}  {names}")
    print(
        "\nOnly the Apache-2.0 ones may be redistributed, with the notice kept. "
        "'unstated' means no LICENSE.txt in the skill folder — treat as unclear."
    )
    if tmp:
        print(f"\nCorpus left at {corpus}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
