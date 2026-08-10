#!/usr/bin/env python3
"""Read a candidate skill the way a strict reviewer would, and say whether a
human should spend time on it.

This agent does not approve anything. Approval needs a person, and that has
not changed. Its job is the opposite one: reject cheaply, so the scarce
resource — someone actually reading the file — is spent on candidates worth
reading. In a queue with one reviewer, the useful machine is the one that
says no early and explains why.

Six axes, scored separately and never collapsed into a single number, because
a collapsed score hides the one thing that matters most here:

  decidable      can the assistant tell whether it followed each step?
  non-obvious    does this encode judgment a competent person needs
                 experience to have, or could anyone improvise it?
  grounded       what does it do when it cannot know?
  contract       is the deliverable specified enough to come out the same twice?
  scope          one task, finished, with its edges named
  safe           nothing that misleads, exfiltrates, or asks for credentials

`non-obvious` is the axis that decides whether the library stays worth
installing from. A method anyone would improvise adds a file and subtracts
attention from the ones that are worth the read.

Three independent passes, each with its own lens. Where they disagree the
disagreement is reported rather than averaged away — a split verdict is
information about the candidate, not noise to smooth out.

  python tools/review_agent.py --rubric        # print the rubric, no API
  python tools/review_agent.py --dry-run       # plan and cost, no API
  python tools/review_agent.py candidates/*.md
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_lint import lint  # noqa: E402

MODEL = "claude-opus-5"
AXES = ["decidable", "non_obvious", "grounded", "contract", "scope", "safe"]

# Three readers, three reasons to reject. Redundant reviewers agree with each
# other; different ones catch different failures.
LENSES = {
    "executor": (
        "You are the assistant that will have to run this skill, on a real task, "
        "for someone who will act on the result. Read it as instructions you must "
        "follow exactly. Where a step leaves you to decide something the file "
        "should have decided, say so and quote the step. Where you would have to "
        "invent a fact to continue, say so."
    ),
    "practitioner": (
        "You are a senior professional in the skill's own field, with fifteen "
        "years of doing this work by hand. Judge whether the method encodes real "
        "judgment or restates the obvious. Name what an expert does that this file "
        "leaves out. Be specific about the missing step, not generally unimpressed."
    ),
    "adversary": (
        "You are looking for reasons this file should be rejected. Assume it looks "
        "competent, because badly written candidates are easy. Hunt for the "
        "confident-sounding step that produces nothing checkable, the output "
        "contract that permits any output, the degradation clause that says "
        "'use judgment', and anything that could mislead a reader who trusts it."
    ),
}

RUBRIC = """Score each axis 1 to 5. Use the whole range; 3 means acceptable, not good.

decidable
  5  every step has an outcome the assistant can verify it produced
  3  most steps are decidable; one or two rest on unstated judgment
  1  the method is a list of intentions ("analyse carefully", "be thorough")

non_obvious
  5  encodes judgment that takes years to acquire: what to look at first,
     what to distrust, the trap that catches beginners
  3  competent and useful, but a careful person would arrive here unaided
  1  restates the task as if it were a method; adds a shape, not knowledge

grounded
  5  states explicitly what to do when a fact, tool or input is missing,
     and forbids filling the gap with a guess
  3  mentions degradation somewhere, without saying what to output instead
  1  silent: the assistant will invent whatever it lacks

contract
  5  the deliverable is specified precisely enough that two runs produce the
     same shape, with sections, order and lengths where they matter
  3  the output is described but leaves the shape open
  1  ten sharp steps and no statement of what comes out

scope
  5  one task, carried to completion, with its edges named
  3  one task, with a vague boundary
  1  several tasks bolted together, or one left half-specified

safe
  5  nothing that could mislead, exfiltrate, request credentials, or hide
     instructions; untrusted input treated as data
  3  no active problem, but a step that processes external content without
     saying it is data
  1  a real hazard: exfiltration, credential requests, hidden content

VERDICT, chosen from the scores and stated separately:
  reject          any axis at 1, or non_obvious at 2 or below
  needs_work      no axis at 1, but at least one below 3
  worth_reading   every axis at 3 or above, and non_obvious at 4 or above
"""

SCHEMA = {
    "type": "object",
    "properties": {
        "scores": {
            "type": "object",
            "properties": {a: {"type": "integer", "minimum": 1, "maximum": 5} for a in AXES},
            "required": AXES,
            "additionalProperties": False,
        },
        "verdict": {"type": "string", "enum": ["reject", "needs_work", "worth_reading"]},
        "strongest_objection": {
            "type": "string",
            "description": "The single most serious problem, quoting the step or section it is in. If there is none, say so plainly.",
        },
        "missing": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Concrete things a reviewer should require before merge. Empty if none.",
        },
        "one_line": {"type": "string", "description": "What this skill is, in the reviewer's own words, at most 20 words."},
    },
    "required": ["scores", "verdict", "strongest_objection", "missing", "one_line"],
    "additionalProperties": False,
}


def read_skill(path: str) -> str:
    return open(path, encoding="utf-8").read()


def judge(client, model: str, lens: str, instruction: str, skill: str) -> dict:
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        system=(
            f"{instruction}\n\nYou are reviewing a candidate for Skills Commons, a library "
            "whose entire value is that a person read every file before it merged. Your "
            "job is to protect that reader's time by rejecting what is not worth their "
            "attention. Be exacting. A candidate that merely looks professional is the "
            "case you exist to catch.\n\n" + RUBRIC
        ),
        messages=[{"role": "user", "content": f"The candidate:\n\n---\n{skill}\n---"}],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("declined by safety classifiers")
    text = next(b.text for b in response.content if b.type == "text")
    out = json.loads(text)
    out["lens"] = lens
    return out


def combine(passes: list[dict]) -> dict:
    """Median per axis, and the disagreement kept rather than smoothed away."""
    scores = {a: int(statistics.median(p["scores"][a] for p in passes)) for a in AXES}
    spread = {a: max(p["scores"][a] for p in passes) - min(p["scores"][a] for p in passes) for a in AXES}
    verdicts = [p["verdict"] for p in passes]

    if any(v == "reject" for v in verdicts):
        verdict = "reject"           # one reader finding a real hazard is enough
    elif all(v == "worth_reading" for v in verdicts):
        verdict = "worth_reading"    # unanimity required to spend a human on it
    else:
        verdict = "needs_work"

    return {
        "scores": scores,
        "spread": spread,
        "verdict": verdict,
        "verdicts": verdicts,
        "contested": [a for a, s in spread.items() if s >= 2],
        "objections": [{"lens": p["lens"], "objection": p["strongest_objection"]} for p in passes],
        "missing": sorted({m for p in passes for m in p["missing"]}),
        "one_line": passes[0]["one_line"],
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="candidate files; defaults to candidates/*.md")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--out", default="review.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--rubric", action="store_true")
    args = ap.parse_args()

    if args.rubric:
        print(RUBRIC)
        print("Lenses:\n")
        for name, text in LENSES.items():
            print(f"  {name}\n    {text}\n")
        return 0

    files = args.files or sorted(glob.glob("candidates/*.md"))
    files = [f for f in files if os.path.basename(f) not in {"README.md", "TOPICS.md"}]
    if not files:
        print("Nothing to review.")
        return 1

    # The cheap gate runs first: a candidate that fails structurally never
    # reaches the expensive one.
    print("Structural gate\n")
    passed = []
    for f in files:
        rep = lint(f, spec_only=True)
        errs = rep.errors
        print(f"  {os.path.basename(f):34} {'blocked: ' + errs[0][2][:48] if errs else 'ok'}")
        if not errs:
            passed.append(f)

    print(f"\n{len(passed)} of {len(files)} reach the reading stage; "
          f"{len(passed) * len(LENSES)} calls on {args.model}")

    if args.dry_run:
        print("\nDry run — nothing was called.")
        return 0

    try:
        import anthropic
    except ImportError:
        print("\nThe anthropic SDK is required: pip install anthropic")
        return 1

    client = anthropic.Anthropic()
    results = []
    print()
    for f in passed:
        skill = read_skill(f)
        passes, failures = [], []
        for lens, instruction in LENSES.items():
            try:
                passes.append(judge(client, args.model, lens, instruction, skill))
            except Exception as exc:  # noqa: BLE001 — recorded, never swallowed
                failures.append(f"{lens}: {type(exc).__name__}: {exc}")
        if len(passes) < 2:
            print(f"  {os.path.basename(f):34} inconclusive — {'; '.join(failures)}")
            continue
        row = combine(passes)
        row["file"] = f
        row["failed_lenses"] = failures
        results.append(row)
        mark = {"reject": "reject      ", "needs_work": "needs work  ", "worth_reading": "worth reading"}[row["verdict"]]
        print(f"  {os.path.basename(f):34} {mark}  non-obvious {row['scores']['non_obvious']}/5"
              + (f"  [contested: {', '.join(row['contested'])}]" if row["contested"] else ""))

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2, ensure_ascii=False)

    print("\n" + "=" * 72)
    for r in sorted(results, key=lambda r: r["scores"]["non_obvious"]):
        print(f"\n{os.path.basename(r['file'])} — {r['verdict']}")
        print(f"  {r['one_line']}")
        print("  " + "  ".join(f"{a.replace('_', '-')} {r['scores'][a]}" for a in AXES))
        if r["contested"]:
            print(f"  readers disagreed on: {', '.join(r['contested'])} — read it yourself before deciding")
        for o in r["objections"]:
            print(f"  [{o['lens']}] {o['objection']}")
        for m in r["missing"]:
            print(f"   - {m}")

    counts = {v: sum(1 for r in results if r["verdict"] == v) for v in ["worth_reading", "needs_work", "reject"]}
    print(f"\n{counts['worth_reading']} worth reading, {counts['needs_work']} need work, "
          f"{counts['reject']} rejected. Written to {args.out}.")
    print("Nothing here merges anything. A verdict of 'worth reading' means a "
          "person should now spend time on it, and nothing more.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
