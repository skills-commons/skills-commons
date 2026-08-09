#!/usr/bin/env python3
"""Measure how much a skill decides, and how much it leaves to the model.

Run one skill several times against the same frozen input and compare the
outputs to each other. Where the file has decided something, every run agrees.
Where it has not, the model fills the gap differently each time — and that gap
is where invention lives.

Three numbers per skill, deliberately not collapsed into one:

  structure  agreement on the shape of the deliverable (headings, labels,
             table columns). Comes from the Output format section doing its job.
  content    agreement on the words themselves, over 3-word shingles. Low
             content with high structure means the shape is fixed and the
             substance is improvised.
  spread     how much the length and the number of listed items move between
             runs, as a coefficient of variation. 0 means identical volume.

This measures repeatability, not correctness. A skill can be consistently
wrong and score 1.00. Correctness stays with the human reviewer.

  python tools/repeatability.py --self-test     # validate the metric, no API
  python tools/repeatability.py --dry-run       # show the plan and the cost
  python tools/repeatability.py --runs 3        # measure (needs credentials)
  python tools/repeatability.py --skills sql-query-reviewer,bug-report-pro
"""

from __future__ import annotations

import argparse
import concurrent.futures
import glob
import itertools
import json
import os
import re
import statistics
import sys

MODEL = "claude-opus-5"
MAX_TOKENS = 8000
FIXTURES = "tests/fixtures"

WORD = re.compile(r"[a-z0-9]+")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", re.M)
BOLD_LABEL = re.compile(r"^\s{0,3}(?:[-*+]\s+)?\*\*(.+?)\*\*", re.M)
TABLE_ROW = re.compile(r"^\s*\|(.+)\|\s*$", re.M)
LIST_ITEM = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+\S", re.M)


# --------------------------------------------------------------------------
# Metrics — pure functions, no API involved. Validated by --self-test.
# --------------------------------------------------------------------------

def words(text: str) -> list[str]:
    return WORD.findall(text.lower())


def shingles(text: str, k: int = 3) -> set[tuple[str, ...]]:
    w = words(text)
    if len(w) < k:
        return {tuple(w)} if w else set()
    return {tuple(w[i : i + k]) for i in range(len(w) - k + 1)}


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def structure_labels(text: str) -> set[str]:
    """The visible skeleton: headings, bold labels, table header cells."""
    labels = {h.strip().lower() for h in HEADING.findall(text)}
    labels |= {b.strip().lower().rstrip(":") for b in BOLD_LABEL.findall(text)}
    rows = TABLE_ROW.findall(text)
    if rows:
        cells = [c.strip().lower() for c in rows[0].split("|") if c.strip()]
        labels |= {c for c in cells if not set(c) <= set("-: ")}
    return {l for l in labels if l}


def mean_pairwise(items: list, fn) -> float:
    pairs = list(itertools.combinations(items, 2))
    if not pairs:
        return 1.0
    return statistics.fmean(fn(a, b) for a, b in pairs)


def cv(values: list[float]) -> float:
    """Coefficient of variation; 0 when every run produced the same amount."""
    vals = [v for v in values if v is not None]
    if len(vals) < 2:
        return 0.0
    mean = statistics.fmean(vals)
    if mean == 0:
        return 0.0
    return statistics.pstdev(vals) / mean


def score(outputs: list[str]) -> dict:
    return {
        "structure": round(mean_pairwise(outputs, lambda a, b: jaccard(structure_labels(a), structure_labels(b))), 3),
        "content": round(mean_pairwise(outputs, lambda a, b: jaccard(shingles(a), shingles(b))), 3),
        "length_cv": round(cv([len(words(o)) for o in outputs]), 3),
        "items_cv": round(cv([len(LIST_ITEM.findall(o)) for o in outputs]), 3),
        "median_words": int(statistics.median([len(words(o)) for o in outputs])) if outputs else 0,
    }


# --------------------------------------------------------------------------
# Running
# --------------------------------------------------------------------------

def skill_body(path: str) -> str:
    text = open(path, encoding="utf-8").read()
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :].lstrip("\n")
    return text


def call_once(client, model: str, effort: str | None, system: str, user: str) -> str:
    kwargs = dict(model=model, max_tokens=MAX_TOKENS, system=system,
                  messages=[{"role": "user", "content": user}])
    if effort:
        kwargs["output_config"] = {"effort": effort}
    # No server-side fallback here on purpose: a fallback would answer with a
    # different model mid-measurement, and the number would then describe two
    # models at once. A refusal is recorded as a failed run instead.
    response = client.messages.create(**kwargs)
    if response.stop_reason == "refusal":
        raise RuntimeError("refused by safety classifiers")
    return "".join(b.text for b in response.content if b.type == "text")


def measure(pairs: list[tuple[str, str]], runs: int, model: str, effort: str | None,
            workers: int) -> list[dict]:
    import anthropic

    client = anthropic.Anthropic()
    results = []
    for name, path in pairs:
        system = skill_body(path)
        user = open(os.path.join(FIXTURES, f"{name}.md"), encoding="utf-8").read()
        outputs, failures = [], []

        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(call_once, client, model, effort, system, user)
                       for _ in range(runs)]
            for fut in futures:
                try:
                    outputs.append(fut.result())
                except Exception as exc:  # noqa: BLE001 - recorded, not swallowed
                    failures.append(f"{type(exc).__name__}: {exc}")

        row = {"skill": name, "runs": len(outputs), "failures": failures}
        row.update(score(outputs) if len(outputs) >= 2 else
                   {"structure": None, "content": None, "length_cv": None,
                    "items_cv": None, "median_words": 0})
        results.append(row)
        print(f"  {name:26} {len(outputs)}/{runs} runs"
              + (f"  [{len(failures)} failed]" if failures else ""))
    return results


# --------------------------------------------------------------------------
# Self-test: proves the metric discriminates, without spending a token.
# --------------------------------------------------------------------------

SAME = "## Decisions\n\n- Ship Thursday (Ana, 2026-08-13)\n\n## Open questions\n\n- Who asks the CFO?\n"
REWORDED = "## Decisions\n\n- Release on Thursday, owned by Ana, due 2026-08-13\n\n## Open questions\n\n- CFO approval still unassigned\n"
DIFFERENT = "Summary\n\nThe team had a long conversation about several topics and reached a few conclusions that may be revisited.\n"


def self_test() -> int:
    checks = []

    identical = score([SAME, SAME, SAME])
    checks.append(("identical runs: structure 1.0", identical["structure"] == 1.0))
    checks.append(("identical runs: content 1.0", identical["content"] == 1.0))
    checks.append(("identical runs: no spread", identical["length_cv"] == 0.0 and identical["items_cv"] == 0.0))

    same_shape = score([SAME, REWORDED])
    checks.append(("same headings, different words: structure stays high", same_shape["structure"] >= 0.9))
    checks.append(("same headings, different words: content drops", same_shape["content"] < 0.5))

    unrelated = score([SAME, DIFFERENT])
    checks.append(("unrelated outputs: structure low", unrelated["structure"] < 0.5))
    checks.append(("unrelated outputs: content low", unrelated["content"] < 0.2))
    checks.append(("unrelated outputs: spread visible", unrelated["items_cv"] > 0.0))

    checks.append(("shingles ignore case and punctuation", shingles("Ship it, now") == shingles("ship it now")))
    checks.append(("empty comparison is not a crash", score(["", ""])["content"] == 1.0))
    checks.append(("single run reports no spread", cv([5]) == 0.0))

    width = max(len(label) for label, _ in checks)
    for label, ok in checks:
        print(f"  {'ok  ' if ok else 'FAIL'} {label:{width}}")
    failed = [label for label, ok in checks if not ok]
    print(f"\n{len(checks) - len(failed)}/{len(checks)} metric checks passed")
    print("\nWorked example — same shape, different substance:")
    print(f"  structure {same_shape['structure']}   content {same_shape['content']}")
    print("  A skill scoring like this has pinned the format and left the substance open.")
    return 1 if failed else 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", type=int, default=3, help="executions per skill (minimum 2)")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--effort", default=None, choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--skills", default=None, help="comma-separated subset")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="repeatability.json")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    pairs = []
    for path in sorted(glob.glob("skills/*/*.md")):
        name = os.path.basename(path)[:-3]
        if args.skills and name not in args.skills.split(","):
            continue
        fixture = os.path.join(FIXTURES, f"{name}.md")
        if not os.path.isfile(fixture):
            print(f"skipping {name}: no fixture at {fixture}")
            continue
        pairs.append((name, path))

    if not pairs:
        print("Nothing to measure — run from the repository root.")
        return 1
    if args.runs < 2:
        print("--runs must be at least 2; the metric compares runs to each other.")
        return 1

    calls = len(pairs) * args.runs
    print(f"{len(pairs)} skill(s) x {args.runs} runs = {calls} calls on {args.model}"
          + (f" at effort {args.effort}" if args.effort else ""))

    if args.dry_run:
        print("\nDry run — nothing was called. Planned:")
        for name, path in pairs:
            body = len(words(skill_body(path)))
            fix = len(words(open(os.path.join(FIXTURES, f'{name}.md'), encoding='utf-8').read()))
            print(f"  {name:26} skill {body:5} words   fixture {fix:4} words")
        return 0

    try:
        import anthropic  # noqa: F401
    except ImportError:
        print("The anthropic SDK is required: pip install anthropic")
        return 1

    print()
    results = measure(pairs, args.runs, args.model, args.effort, args.workers)

    payload = {"model": args.model, "effort": args.effort, "runs": args.runs, "results": results}
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)

    print(f"\n{'skill':26} {'structure':>10} {'content':>8} {'len cv':>7} {'items cv':>9} {'words':>6}")
    scored = [r for r in results if r["structure"] is not None]
    for r in sorted(scored, key=lambda r: r["content"]):
        print(f"{r['skill']:26} {r['structure']:10} {r['content']:8} "
              f"{r['length_cv']:7} {r['items_cv']:9} {r['median_words']:6}")
    if scored:
        print(f"\nmedian structure {statistics.median(r['structure'] for r in scored):.3f}"
              f"   median content {statistics.median(r['content'] for r in scored):.3f}")
    skipped = [r for r in results if r["structure"] is None]
    if skipped:
        print(f"\n{len(skipped)} skill(s) had fewer than 2 successful runs:")
        for r in skipped:
            print(f"  {r['skill']}: {'; '.join(r['failures'][:2])}")
    print(f"\nWritten to {args.out}. Repeatability, not correctness.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
