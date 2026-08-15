# Run retro protocol

Executed by the boss at the end of EVERY foreman run, after the cost table. The run
is not done until the retro is written. Ledgers: `lessons.md` here (portable) +
repo-local `foreman-notes.md` (repo-specific intel: build commands, shared-tree
hazards, which pages/modules are safe to parallelize).

## Run section template (append to ledger)

```markdown
## Run <n> — <date> — <one-line job description>

**Job**: <what was built>  **Setup**: <constitution size, cards, bands>

| Agent | Band | Card size (files listed / inline lines) | Result |
|---|---|---|---|
| <name> | <band> | <n> files / <n> inline | passed / died-<reason> / failed-<reason> |

**Worked**: <bullets — only things with evidence>
**Failed**: <bullets — symptom, then verified cause; UNKNOWN if the idle
  notification never explained it. Never backfill a plausible cause.>
**Confounds**: <anything correlated that blocks a conclusion, named explicitly>
**Artifacts per token**: <delivered artifacts vs spend; which band carried the load>
**Documented fixes applied mid-run**: <lesson id → did it work? yes/no>
```

## Lesson lifecycle

Each lesson in `lessons.md` carries: `id`, `status`, `evidence` (run refs), `rule`
(one sentence, imperative), and if promoted, `landed-in` (file + section).

- **CANDIDATE** — seen once. Applied opportunistically next run, not yet law.
- **ACTIVE / PROMOTED** — confirmed twice across runs, or once with an airtight
  causal chain. The boss edits SKILL.md / references directly, date-stamps the
  edit, records `landed-in`.
- **DEMOTED** — contradicted later. Record the counter-evidence, revert the
  promoted edit. Never silently delete: a demoted lesson is data about the skill's
  own error rate.
- **UNANSWERED** — a question a run raised but did not settle (e.g. "is ECONOMY
  actually more reliable, or was it card size?"). Stays listed until a controlled
  run answers it. Absence of an answer never becomes a conclusion.

## Self-edit guardrails (checked before every promotion edit)

1. Does the edit weaken any verification/safety rule (execute-don't-read, checker
   independence, context budget, build scoping)? → STOP; those only tighten, or go
   through the user.
2. Does the new rule cite the run(s) that earned it? No citation, no rule.
3. If the rule adds a check, was it negative-tested (one concrete example that
   would have FAILed under it)?
4. Size caps: SKILL.md ≤200 lines, each reference ≤250. At the cap, compress
   existing text before adding.
5. Is a confound being promoted as if it were a conclusion? → It stays a
   CANDIDATE + UNANSWERED question instead.
