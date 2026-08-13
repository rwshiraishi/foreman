---
name: foreman
description: Operational multi-agent dispatch for app, software, and website builds — actually spawns the org chart rather than advising on it. A boss (frontier model) writes the spec and constitution, reviews, and arbitrates but never implements; cheap workers (haiku/sonnet) do all implementation; every task gets an independent checker that executes the work (builds, tests, fetches, renders) and never trusts the worker's self-report; failures loop back with specific feedback until they pass; a final adversarial skeptic attacks the assembled build before done. Discovers available models at runtime and assigns tiers automatically. Use when the user says "run the foreman", "orchestrate this build", "use cheap models for the easy parts", "boss/worker pattern", "build this with tiered agents", or invokes /model-route, and the job decomposes into 3+ independently verifiable tasks. Standalone: no other skills required.
---

# Foreman

Boss specs and inspects; workers build; checkers execute-and-verify. Nobody's word is trusted — every claim is checked by running the thing.

## 1. When to use / when not

Use when the job decomposes into **3+ independently verifiable tasks** (each with a testable done-condition). Do NOT use when:
- The whole job fits in ≤2 files / <100 changed lines — just do it in-session; orchestration overhead exceeds the work.
- The user is mid-flow debugging — session continuity beats dispatch.
- Coordination cost would exceed implementation cost (see §9).

This skill is how CLAUDE.md's mandates get staffed (parallel-first subagents, verification-before-done, language reviewers before commit) — it composes with them, never bypasses them.

## 2. Model discovery + research (automatic — never ask the user which model)

Never hardcode a model roster. At run start:

1. **Discover** the dispatchable set:
   - Session environment facts (current model, latest model families listed in the system prompt).
   - The Agent tool's `model` enum (currently `sonnet | opus | haiku | fable`).
   - The Workflow tool's `agent(prompt, {model, effort})` — `effort: low|medium|high|xhigh|max` multiplies the ladder (a sonnet at high effort can outperform a lazy opus for structured tasks).
   - Optional: `curl -s https://api.anthropic.com/v1/models -H "x-api-key: $ANTHROPIC_API_KEY" -H "anthropic-version: 2023-06-01"` when a key is set.
2. **Consult the intel cache**: read `references/model-intel.md`. If `last-verified` is >30 days old, or discovery found a model not in the table, refresh it: spawn 1-2 ECONOMY research agents (WebSearch: current per-model pricing $/Mtok, coding-benchmark standing, context limits) and rewrite the table with a new date stamp. Research is itself cheap-tier work.
3. **Map to bands, not names**:

   | Band | Role | Typical (per intel table) |
   |---|---|---|
   | FRONTIER | boss: spec, constitution, arbitration, final review | session model (fable/opus) |
   | STANDARD | implementation workers, logic checkers | sonnet |
   | ECONOMY | mechanical workers, format/compare checkers, research | haiku |

   All assignment logic below uses bands; concrete model names appear only in the run's cost report. New model releases update the intel table, never this file.
4. The only user knob is `--budget low|med|high` (low: workers capped at ECONOMY, checkers at STANDARD; high: FRONTIER arbitration rounds permitted). Everything else is decided automatically.

## 3. Task classification → band

Operationally:

| Task class | Worker band |
|---|---|
| Boilerplate, copy, config, narrow single-file edits, classification, research | ECONOMY |
| Implementation, refactors, tests, integration | STANDARD |
| Architecture, spec-writing, root-cause analysis, multi-file invariants, arbitration | FRONTIER (boss only — never a worker) |

**Checker band rule**: checker ≥ worker band for logic/behavior checks; ECONOMY checkers are fine for mechanical verification (character-compare, file-exists, build-exit-code). Escalate a band only on a clear reasoning gap at the lower band, never on a first failure.

## 4. The org chart

**Boss** (FRONTIER; usually the session model — you). Writes the spec, the constitution (§5), and the task decomposition; reviews checker verdicts; arbitrates disputes. **NEVER implements.** Its outputs are documents and decisions — and they are themselves checked: before dispatch, a STANDARD agent verifies the spec is internally consistent and every task has a testable done-condition. A boss spec that fails this check gets fixed before any worker spawns.

**Workers** (ECONOMY/STANDARD per §3). Each receives exactly one task card (§6) + the constitution. A worker's "done" is a **claim**, never a fact.

**Skeptic** (STANDARD or FRONTIER; exactly one per run). Spawned after all tasks pass their checkers, before the boss declares done. Its brief is pure refutation: assume the build is broken and prove it — attack the assembled whole (integration seams between tasks, the gaming patterns in §9, constitution clauses nobody's checker owned, the checks themselves). It gets the constitution and the checkers' verdicts, and is scored on finding real breaks, not on agreeing. **It reports to the boss and only to the boss** — it never messages workers, never dispatches fixes, and never declares the run done itself. The boss adjudicates each finding (a skeptic can be wrong too; the §7 dispute path and rubric-amendment rule apply to its findings exactly as to a checker's), then routes accepted findings into the owning task's loop as feedback. Findings the boss rejects are recorded with the reason, not silently dropped. Distinct from checkers: checkers verify one task's done-condition; the skeptic hunts what no single done-condition covers.

**Checkers** (independent, decorrelated). Decorrelation ladder: prefer **CROSS-TIER** (a different Claude band via the model override), fall back to **SAME-MODEL** and label it honestly in the run log. Checkers **execute**:
- Code: run the build, run the tests, run the linter — read exit codes, not diffs.
- Web: fetch the URL, render the page (webapp-testing / browse skills), test both themes.
- Content: character-compare protected text against the source, refetch cited URLs.
- A checker that only read the diff and agreed has failed its job. Verdicts are structured: `{verdict, evidence[], repro_command, feedback}`.

## 5. The constitution

Before any dispatch, the boss writes a one-page done-right standard for THIS build: stack conventions, quality floor (a11y/security/test coverage), forbidden shortcuts, and the exact verification command per task type. Derive it from CLAUDE.md + the repo; ask the user only what is underivable, in one batched round. Template: `references/constitution-template.md`.

Every worker and checker prompt embeds the constitution. Checkers grade against it, not vibes. Per-task instructions shrink to "task card + constitution". When a checker is proven wrong (§7), the fix is a constitution amendment, so the whole fleet learns.

## 6. Dispatch mechanics — every spawn is fully spec'd

**Tool choice**: Agent tool for ≤4 tasks or when the user should review between rounds (explicit `model:` on every call — never inherit silently). Workflow tool for 5+ tasks, retry loops, or budget enforcement; the user invoking this skill is the required orchestration opt-in.

**No bare instructions.** Every worker spawn carries a boss-authored **task card**:
- Objective (one sentence) · Inputs (exact file paths + relevant spec excerpt) · Done-condition (testable, from the spec) · Verification command the checker will run · Required output schema `{status, evidence, files_touched}` · The constitution.

Checkers get the matching card plus the worker's claim — never the worker's reasoning (that would correlate their errors).

Prefer existing specialized agents via `subagent_type` + model override (e.g. `typescript-reviewer` as a STANDARD checker) over generic agents. Parallel workers mutating files use worktree isolation. Copy-paste call shapes for both tools: `references/call-shapes.md`.

**Communication contract (both directions, during the build):**
- Every worker/checker/skeptic prompt ends with the reporting clause: on completion, SendMessage your result JSON to `main` — an idle notification without the JSON is an incomplete report. If a spawned agent goes idle without delivering, the boss requests the result by name once before considering the task stalled.
- **Worker → boss, mid-task**: workers are told to SendMessage `main` immediately when blocked, when the spec is ambiguous, or when two constitution clauses conflict — and to STOP rather than guess. A question costs one message; a guessed-wrong implementation costs a full retry loop.
- **Boss → worker, mid-task**: the boss pushes spec corrections and constitution amendments to affected named workers via SendMessage as soon as they're ratified — workers must not learn about an amendment from a FAIL verdict.
- Spawn workers with `name:` so they stay addressable for retries, amendments, and disputes; keep all coordination through the boss (workers never message each other — sibling chatter correlates errors and bypasses arbitration).

## 7. Verification loop

Per task: worker → checker executes → **PASS** (evidence attached) or **FAIL** (specific and reproducible: command run, expected, actual) → same worker retries **with the feedback** → max 2 retries at band → escalate worker band once → then boss decides.

**Disputes**: a worker may contest a verdict. The boss arbitrates with both outputs in hand. If the checker was wrong, amend the checker's rubric in the constitution — don't just flip the verdict. Verification runs in both directions: boss outputs pass through a checker too, and rank exempts nobody.

**Stop condition**: 3 boss arbitrations on the same task → stop and surface to the user with both sides. Never loop past that.

**Final gate**: when every task has PASSed, the skeptic (§4) runs against the assembled build and reports to the boss. The boss adjudicates, routes accepted findings into the owning task's loop as feedback, and re-runs the skeptic on the fixed build — briefing it on what changed and on any new risk the fix introduces (a guard added to stop one failure is a prime suspect for swallowing a legitimate case). Re-runs also re-verify that the fix's own tests actually fail against deliberately broken code, or the coverage is a mirage. Only the boss declares done, and only on a skeptic pass with executed attacks logged.

## 8. Cost accounting

End every run with a table: tasks per band, concrete models used, retries, escalations, and estimated spend vs an all-FRONTIER baseline (prices from `references/model-intel.md`). The user should see whether the cheap bands actually carried the load.

## 9. Failure modes

| Symptom | Response |
|---|---|
| Checker fails constitution-compliant work repeatedly | Dispute path (§7); amend rubric |
| Worker games the check: hidden text, hardcoded expected values, skipped/disabled tests | Checkers verify *mechanism*, not just output — grep for `skip`/`display:none`/hardcoded fixtures; the check checks the check |
| Correlated errors (worker and checker share priors) | Prefer CROSS-TIER checkers; never let a worker's same-band sibling check the same task it could have written |
| Coordination messages exceed implementation work | Collapse to in-session execution, tell the user, and log why |

## Companion documents

- **references/call-shapes.md** — copy-paste dispatch: task cards, worker/checker/skeptic spawns, comms contract
- **references/constitution-template.md** — the done-right standard, with a worked example
- **references/model-intel.md** — model → band/price/strengths, date-stamped and refreshable

If your setup has skills for advisory model-tier doctrine, competing-solution scoring, single-task verification, or browser-driven testing, Foreman composes with them: it handles dispatch and they handle their own domains.
