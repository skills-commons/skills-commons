#!/usr/bin/env python3
"""Structural checks for Skills Commons skill files.

Every check here is deterministic: it reads the file and compares it to a
rule stated in SPEC.md or SECURITY.md. Nothing in this script judges whether
a method is *good* — that is the reviewer's job, and no keyword count is a
substitute for it.

Severity:
  error  — the file breaks a stated rule; the claim is checkable from the text
  warn   — worth a human glance; a legitimate file can trip these

Usage:
  python tools/skill_lint.py                 # every skill in skills/
  python tools/skill_lint.py FILE [FILE...]  # named files
  python tools/skill_lint.py --annotate      # also emit GitHub annotations
"""

from __future__ import annotations

import os
import re
import sys
import glob

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

CATEGORIES = {"agents", "engineering", "workplace", "writing"}
REQUIRED_KEYS = ["name", "description", "version", "license"]
SPEC_KEYS = ["name", "description"]  # Agent Skills specification minimum
REQUIRED_SECTIONS = ["Inputs", "Method", "Output format", "Rules"]

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
# Zero-width, bidi overrides and other invisibles used to hide instructions.
INVISIBLE = re.compile(r"[​-‏‪-‮⁠-⁤﻿]")
BLOB = re.compile(r"[A-Za-z0-9+/]{60,}={0,2}")
URL = re.compile(r"https?://[^\s)\]>\"']+")
CREDENTIAL = re.compile(
    r"\b(api[ _-]?key|access[ _-]?token|password|client[ _-]?secret|"
    r"private[ _-]?key|credential)s?\b",
    re.I,
)
DECLARED_STEPS = re.compile(r"\b(\d+)[- ]steps?\b", re.I)
NUMBERED = re.compile(r"^(\d+)\.\s+\S", re.M)


class Report:
    """Findings for one file.

    Two rule sets live here. The Agent Skills specification
    (https://agentskills.io/specification) applies to any skill anywhere;
    the house rules come from this library's own SPEC.md. `spec_only`
    keeps the second set quiet so an outside corpus can be measured on the
    same terms as ours.
    """

    def __init__(self, path: str, spec_only: bool = False):
        # Forward slashes so GitHub annotations resolve on every runner.
        self.path = path.replace("\\", "/")
        self.spec_only = spec_only
        self.findings: list[tuple[str, str, str, int | None]] = []

    def error(self, code, msg, line=None):
        self.findings.append(("error", code, msg, line))

    def warn(self, code, msg, line=None):
        self.findings.append(("warn", code, msg, line))

    def house_error(self, code, msg, line=None):
        if not self.spec_only:
            self.error(code, msg, line)

    def house_warn(self, code, msg, line=None):
        if not self.spec_only:
            self.warn(code, msg, line)

    @property
    def errors(self):
        return [f for f in self.findings if f[0] == "error"]

    @property
    def warnings(self):
        return [f for f in self.findings if f[0] == "warn"]


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def split_frontmatter(text: str):
    """Return (frontmatter_str, body_str, body_offset) or (None, text, 0)."""
    if not text.startswith("---"):
        return None, text, 0
    end = text.find("\n---", 3)
    if end == -1:
        return None, text, 0
    fm = text[3:end]
    after = text[end + 4 :]
    return fm, after, len(text) - len(after)


def sections(body: str) -> dict[str, str]:
    """Map '## Heading' -> the text under it, up to the next '## '."""
    out: dict[str, str] = {}
    parts = re.split(r"^## +(.+?)\s*$", body, flags=re.M)
    for i in range(1, len(parts), 2):
        out[parts[i].strip()] = parts[i + 1]
    return out


def check_path(path: str, rep: Report) -> str | None:
    norm = path.replace("\\", "/")
    m = re.search(r"skills/([^/]+)/([^/]+)\.md$", norm)
    if not m:
        rep.house_error("P001", "File must live at skills/<category>/<name>.md")
        return None
    category, stem = m.group(1), m.group(2)
    if category not in CATEGORIES:
        rep.house_error(
            "P002",
            f"Unknown category '{category}' — expected one of "
            + ", ".join(sorted(CATEGORIES))
            + " (propose a new one in the pull request)",
        )
    return stem


def check_frontmatter(fm: str | None, stem: str | None, text: str, rep: Report):
    if fm is None:
        rep.error("F001", "No YAML frontmatter delimited by --- at the top of the file", 1)
        return None
    try:
        data = yaml.safe_load(fm)
    except yaml.YAMLError as exc:
        first = str(exc).splitlines()[0]
        rep.error("F002", f"Frontmatter is not valid YAML: {first}", 1)
        return None
    if not isinstance(data, dict):
        rep.error("F002", "Frontmatter must be a mapping of keys to values", 1)
        return None

    keys = SPEC_KEYS if rep.spec_only else REQUIRED_KEYS
    for key in keys:
        if key not in data or data[key] in (None, ""):
            rep.error("F003", f"Frontmatter is missing '{key}'")

    name = data.get("name")
    if isinstance(name, str):
        if not KEBAB.match(name):
            rep.error("F004", f"name '{name}' must be kebab-case: a-z, 0-9 and single hyphens")
        elif stem and name != stem and not rep.spec_only:
            rep.error("F005", f"name '{name}' must match the filename '{stem}.md'")
        if len(name) > 64:
            rep.error("F010", f"name is {len(name)} characters; the Agent Skills spec caps it at 64")
    elif name is not None:
        rep.error("F004", "name must be a string")

    version = data.get("version")
    if version is not None:
        if not isinstance(version, str):
            rep.house_error("F006", f"version must be a quoted string, e.g. \"1.0.0\" (got {version!r})")
        elif not SEMVER.match(version):
            rep.house_error("F006", f"version '{version}' is not semver (major.minor.patch)")

    lic = data.get("license")
    if lic is not None and lic != "Apache-2.0":
        rep.house_warn("F007", f"license is '{lic}'; the library ships Apache-2.0")

    desc = data.get("description")
    if isinstance(desc, str) and desc.strip():
        flat = " ".join(desc.split())
        if len(flat) > 1024:
            rep.error("F011", f"description is {len(flat)} characters; the Agent Skills spec caps it at 1024")
        if len(flat) < 60:
            rep.house_warn("F008", f"description is {len(flat)} characters — say what it does and when to use it")
        # Whether the description states a usable trigger is a semantic property.
        # A check for the literal word "when" flags every skill written as
        # "Use for ..." — which is most of this library. Left to human review.
    return data


def check_body(body: str, offset: int, text: str, rep: Report):
    if not re.search(r"^# +\S", body, re.M):
        rep.house_error("B001", "No '# Title' heading after the frontmatter")

    found = sections(body)
    for want in REQUIRED_SECTIONS:
        match = next((k for k in found if k.lower() == want.lower()), None)
        if match is None:
            rep.house_error("B002", f"Missing required section '## {want}' (SPEC.md)")
        elif not found[match].strip():
            rep.house_error("B003", f"Section '## {match}' is empty")

    words = len(body.split())
    if words < 150:
        rep.house_warn("B004", f"{words} words — likely under-specified for a reviewable method")
    elif words > 1500:
        rep.house_warn("B004", f"{words} words — long enough that instructions start competing")

    method_key = next((k for k in found if k.lower() == "method"), None)
    steps = []
    if method_key:
        steps = NUMBERED.findall(found[method_key])
        if not steps:
            rep.house_warn("B005", "Method has no numbered steps — SPEC.md asks for numbered steps or checks")
        else:
            numbers = [int(n) for n in steps]
            if numbers != list(range(1, len(numbers) + 1)):
                rep.house_warn("B006", f"Method numbering runs {numbers} — expected 1..{len(numbers)}")

    for m in DECLARED_STEPS.finditer(body):
        declared = int(m.group(1))
        if steps and declared != len(steps):
            rep.house_warn(
                "C001",
                f"Text says '{m.group(0)}' but Method lists {len(steps)} — "
                "confirm the count refers to something else",
                line_of(text, offset + m.start()),
            )
    return found


def check_safety(text: str, rep: Report):
    for m in INVISIBLE.finditer(text):
        rep.error(
            "S001",
            f"Invisible character U+{ord(m.group(0)):04X} — instructions must be readable (SECURITY.md)",
            line_of(text, m.start()),
        )
        break
    for m in BLOB.finditer(text):
        rep.error(
            "S002",
            f"{len(m.group(0))}-character unbroken token, the shape of encoded content (SECURITY.md)",
            line_of(text, m.start()),
        )
        break
    for m in URL.finditer(text):
        rep.warn(
            "S003",
            f"Contains {m.group(0)[:60]} — a skill must be complete as written, never fetching "
            "instructions at runtime (SECURITY.md)",
            line_of(text, m.start()),
        )
        break

def check_inputs_for_credentials(found: dict[str, str], body: str, offset: int, text: str, rep: Report):
    """A skill may discuss credentials; it may not ask the user for one.

    Only the Inputs section states what the user is asked to hand over, so the
    check is scoped there. Matching the whole file flags "never paste an API
    key" — advice, not a request.
    """
    key = next((k for k in found if k.lower() == "inputs"), None)
    if not key:
        return
    section = found[key]
    m = CREDENTIAL.search(section)
    if m:
        at = body.find(section)
        rep.warn(
            "S004",
            f"Inputs asks for '{m.group(0)}' — skills never request credentials (SPEC.md)",
            line_of(text, offset + at + m.start()) if at >= 0 else None,
        )


def lint(path: str, spec_only: bool = False) -> Report:
    rep = Report(path, spec_only)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    stem = check_path(path, rep)
    fm, body, offset = split_frontmatter(text)
    data = check_frontmatter(fm, stem, text, rep)
    found = check_body(body, offset, text, rep)
    check_safety(text, rep)
    check_inputs_for_credentials(found, body, offset, text, rep)
    rep.name = (data or {}).get("name")
    return rep


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    annotate = "--annotate" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        paths = sorted(glob.glob("skills/*/*.md"))
    if not paths:
        print("No skill files found.")
        return 0

    spec_only = "--spec-only" in argv
    reports = [lint(p, spec_only) for p in paths]

    seen: dict[str, str] = {}
    for rep in reports:
        name = getattr(rep, "name", None)
        if isinstance(name, str):
            if name in seen:
                rep.house_error("X001", f"Duplicate skill name '{name}', already used by {seen[name]}")
            else:
                seen[name] = rep.path

    lines = ["| file | level | code | finding |", "| --- | --- | --- | --- |"]
    n_err = n_warn = 0
    for rep in reports:
        for level, code, msg, line in rep.findings:
            where = f"{rep.path}" + (f":{line}" if line else "")
            lines.append(f"| `{where}` | {level} | {code} | {msg} |")
            if level == "error":
                n_err += 1
            else:
                n_warn += 1
            if annotate:
                kind = "error" if level == "error" else "warning"
                pos = f",line={line}" if line else ""
                print(f"::{kind} file={rep.path}{pos}::{code}: {msg}")

    header = f"**{len(reports)} skill file(s) checked — {n_err} error(s), {n_warn} warning(s).**"
    body = header + ("\n\nNothing structural to report." if n_err + n_warn == 0 else "\n\n" + "\n".join(lines))
    body += (
        "\n\nThese checks are structural only. They say nothing about whether the method is any "
        "good — that is what the human review is for."
    )

    print(body)
    for arg in argv:
        if arg.startswith("--report="):
            with open(arg.split("=", 1)[1], "w", encoding="utf-8") as fh:
                fh.write(body + "\n")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(body + "\n")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as fh:
            fh.write(f"errors={n_err}\nwarnings={n_warn}\n")

    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
