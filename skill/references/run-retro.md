# Run retro protocol

Executed by the boss at the end of EVERY foreman run, after the cost table. The run
is not done until the retro is written. Ledgers: `lessons.md` here (portable) +
repo-local `foreman-notes.md` (repo-specific intel: build commands, shared-tree
hazards, which pages/modules are safe to parallelize).

## Run section template (append to ledger)

```markdown
## Run <n> — <date> — <one-line job description>

**Job**: <what was built>  **Setup**: <constitution size, cards, bands>
**Targeting**: <which UNANSWERED question (U-id) this run's setup attempts to
settle, or "none apply" — never blank. Open questions close only when a run aims at them.>

| Agent | Band | Card size (files listed / inline lines) | Result |
|---|---|---|---|
| <name> | <band> | <n> files / <n> inline | passed / died-<reason> / failed-<reason> |

**Deaths** (fill even when empty — "0 deaths" is a data point):

| Agent | Card lines | Files listed | Commands redirected? | Retry depth | Cause class |
|---|---|---|---|---|---|
| <name> | <n> | <n> | yes/no/partial | <n> | context / bundling / infra-flake / unknown |

Context is this skill's most expensive failure mode and the loop only learns about it if
deaths are counted with their card metrics attached. `unknown` is an allowed value; a
guessed cause is not (L4 — never backfill a plausible cause).

**Worked**: <bullets — only things with evidence>
**Failed**: <bullets — symptom, then verified cause; UNKNOWN if the idle
  notification never explained it. Never backfill a plausible cause.>
**Confounds**: <anything correlated that blocks a conclusion, named explicitly>
**Artifacts per token**: <delivered artifacts vs spend; which band carried the load>
**Documented fixes applied mid-run**: <lesson id → did it work? yes/no>
```

## Lesson lifecycle

`lessons.md` is a one-row-per-lesson INDEX: `id`, `status`, `rule` (one imperative
sentence), `landed-in`. The evidence, mechanism, and negative test live in
`lessons-evidence.md` under the same id. Split this way so the pre-run read stays
bounded while the evidence stays complete — evidence is never deleted to fit a cap.

- **CANDIDATE** — seen once. Applied opportunistically next run, not yet law.
- **ACTIVE / PROMOTED** — confirmed twice across runs, or once with an airtight
  causal chain. **"Airtight" is decidable, not vibes — all four must hold**:
  (1) the mechanism fits in one sentence and is fully understood;
  (2) it is independent of this repo/language/tool;
  (3) a negative test exists — the concrete example that WOULD have shipped;
  (4) no named confound offers a competing explanation.
  Fewer than four → stays CANDIDATE. The boss edits SKILL.md / references
  directly, date-stamps the edit, records `landed-in` — and a STANDARD agent
  reviews the promotion diff against the guardrails below before commit (the
  boss's memory edits are not exempt from checking).
- **DEMOTED** — contradicted later. Record the counter-evidence, revert the
  promoted edit. Never silently delete: a demoted lesson is data about the skill's
  own error rate.
- **UNANSWERED** — a question a run raised but did not settle (e.g. "is ECONOMY
  actually more reliable, or was it card size?"). Stays listed until a controlled
  run answers it. Absence of an answer never becomes a conclusion.

## Close-out (the run is NOT done until these have run)

```bash
python3 ~/.claude/skills/foreman/tools/lint.py \
  && git -C ~/.claude add skills/foreman \
  && git -C ~/.claude commit -m "docs(foreman): run <n> retro — <one-line outcome>" \
  && git -C ~/.claude push
```
The `&&` chain is deliberate: the linter's exit code gates the commit. It checks size caps,
index↔evidence ID sync, duplicate IDs, PROMOTED-without-landed-in, the card template's
first line (L18), cross-file references, and that UNANSWERED is non-empty — every check
reports its examined-count and fails at zero (the linter obeys L9). It was negative-tested
at creation: a seeded fake lesson row produced 2 violations; removing it produced 0.

`lessons.md` and this file sat UNTRACKED in git for the skill's entire history (L40) — the
whole memory of the self-improving loop was one machine failure from being lost, because no
step said to commit it. An uncommitted promotion is a lesson learned and thrown away.

## Self-edit guardrails (checked before every promotion edit)

1. Does the edit weaken any verification/safety rule (execute-don't-read, checker
   independence, context budget, build scoping)? → STOP; those only tighten, or go
   through the user.
2. Does the new rule cite the run(s) that earned it? No citation, no rule.
3. If the rule adds a check, was it negative-tested (one concrete example that
   would have FAILed under it)?
4. Size caps: SKILL.md ≤200; `lessons.md` ≤120 and `boss-discipline.md` ≤250 (both
   read pre-run); other references ≤250; `lessons-evidence.md` ≤450 (outside the
   pre-run budget). At a cap, compress or move evidence to `lessons-evidence.md` —
   never drop a lesson. New lesson IDs are never reused.
5. Is a confound being promoted as if it were a conclusion? → It stays a
   CANDIDATE + UNANSWERED question instead.
