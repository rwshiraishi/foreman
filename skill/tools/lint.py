#!/usr/bin/env python3
"""Foreman skill self-lint. Run at every retro close-out (run-retro.md) and after
any hand edit. Exit 0 = clean. Exit 1 = violations printed. Every check reports its
examined-count and fails at zero (L9 — this linter obeys the rule it enforces)."""
import re, sys, collections, os

# Resolve relative to THIS file, not a hardcoded home path: the skill ships in a public
# repo under skill/ and installs to ~/.claude/skills/foreman — a hardcoded root would check
# the wrong tree (or none) for anyone who cloned it, which is the examines-nothing class
# this linter exists to catch.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "references")
CAPS = {"SKILL.md": 200, "references/lessons.md": 120, "references/boss-discipline.md": 250,
        "references/lessons-evidence.md": 450, "references/context-budget.md": 250,
        "references/call-shapes.md": 250, "references/constitution-template.md": 250,
        "references/run-retro.md": 250, "references/model-intel.md": 250}
errs, checked = [], 0

def read(rel):
    with open(os.path.join(ROOT, rel)) as f: return f.read()

# 1. size caps
for rel, cap in CAPS.items():
    n = len(read(rel).splitlines()); checked += 1
    if n > cap: errs.append(f"CAP: {rel} is {n}/{cap} lines")
if checked == 0: errs.append("VACUOUS: no files examined for caps")

# 2. lesson ID sync between index and evidence
idx = re.findall(r"^\| (L\d+b?) \|", read("references/lessons.md"), re.M)
ev  = re.findall(r"^## (L\d+b?) —", read("references/lessons-evidence.md"), re.M)
if not idx or not ev: errs.append("VACUOUS: no lesson IDs found")
for d in [k for k, v in collections.Counter(ev).items() if v > 1]:
    errs.append(f"DUP: {d} appears twice in lessons-evidence.md")
for d in [k for k, v in collections.Counter(idx).items() if v > 1]:
    errs.append(f"DUP: {d} appears twice in lessons.md")
for m in sorted(set(idx) - set(ev)): errs.append(f"SYNC: {m} in index, no evidence entry")
for m in sorted(set(ev) - set(idx)): errs.append(f"SYNC: {m} in evidence, no index row")

# 3. every PROMOTED index row names a landing site
rows = [l for l in read("references/lessons.md").splitlines() if l.startswith("| L")]
if not rows: errs.append("VACUOUS: no index rows examined")
for l in rows:
    if "PROMOTED" in l and l.rsplit("|", 2)[1].strip() in ("—", ""):
        errs.append(f"LANDED-IN missing: {l.split('|')[1].strip()}")

# 4. card template: output discipline is the FIRST line after the header (L18)
tmpl = read("references/call-shapes.md").split("TASK CARD #<n>")
if len(tmpl) < 2: errs.append("TEMPLATE: card template not found")
elif not tmpl[1].splitlines()[1].lstrip().startswith("Output discipline (FIRST"):
    errs.append("TEMPLATE: output discipline is not the card's first line (violates L18)")

# 5. every references/*.md mentioned anywhere actually exists
allt = "".join(read(f"references/{f}") for f in os.listdir(R) if f.endswith(".md")) + read("SKILL.md")
refs = set(re.findall(r"references/([a-z-]+\.md)", allt))
if not refs: errs.append("VACUOUS: no cross-references examined")
for r in refs:
    if not os.path.exists(os.path.join(R, r)): errs.append(f"BROKEN REF: references/{r}")

# 6. UNANSWERED section exists and is non-empty (absence of questions is suspicious, not clean)
if not re.search(r"^## UNANSWERED\n+- \*\*U\d+", read("references/lessons.md"), re.M):
    errs.append("UNANSWERED: section missing or empty — open questions never all close at once")

if errs:
    print(f"FAIL — {len(errs)} violation(s):"); [print("  " + e) for e in errs]; sys.exit(1)
print(f"OK — caps({len(CAPS)}) ids({len(idx)}) refs({len(refs)}) template(1) all clean")
