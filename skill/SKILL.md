---
name: foreman
description: Operational multi-agent dispatch for app, software, and website builds — actually spawns the org chart rather than advising on it. A boss (frontier model) writes the spec and constitution, reviews, and arbitrates but never implements; cheap workers (haiku/sonnet) do all implementation; every task gets an independent checker that executes the work (builds, tests, fetches, renders) and never trusts the worker's self-report; failures loop back with specific feedback until they pass; a final adversarial skeptic attacks the assembled build before done. Discovers available models at runtime and assigns tiers automatically. Use when the user says "run the foreman", "orchestrate this build", "use cheap models for the easy parts", "boss/worker pattern", "build this with tiered agents", or invokes /model-route, and the job decomposes into 3+ independently verifiable tasks. For advisory tier-mapping doctrine see agentic-engineering; for scoring competing solutions see solution-tournament.
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
4. The only user knob is budget: `low` (workers capped at ECONOMY, checkers at STANDARD), `med` (**default when the user says nothing**), `high` (FRONTIER arbitration rounds permitted). Parse it from natural language ("keep it cheap" → low, "spare no expense" → high) — there is no flag syntax to wait for. Everything else is decided automatically.

## 3. Task classification → band

Canonical task-type mapping lives in the `agentic-engineering` skill — do not re-derive it. Operationally:

| Task class | Worker band |
|---|---|
| Boilerplate, copy, config, narrow single-file edits, classification, research | ECONOMY |
| Implementation, refactors, tests, integration | STANDARD |
| Architecture, spec-writing, root-cause analysis, multi-file invariants, arbitration | FRONTIER (boss only — never a worker) |

**Checker band rule**: checker ≥ worker band for logic/behavior checks; ECONOMY checkers are fine for mechanical verification (character-compare, file-exists, build-exit-code). **For STANDARD workers this means SAME-MODEL logic checkers by construction** (FRONTIER is scoped to the boss) — expected, not a fallback failure; label it honestly and decorrelate by effort instead (checker at `effort: high` vs worker at `medium`) and by withholding the worker's reasoning. Escalate a band only on a clear reasoning gap at the lower band, never on a first failure.

## 4. The org chart

**Boss** (FRONTIER; usually the session model — you). Writes the spec, the constitution (§5), and the task decomposition; reviews checker verdicts; arbitrates disputes. **NEVER implements — with exactly one exception: kernel work** (the tenant-context wrapper, the auth boundary, the money path — see `boss-discipline.md` §14). Those are built by the boss, in-session, serially, test-first: they are small, everything depends on them, and a retry loop on them costs more than writing them. Its outputs are documents and decisions — and they are themselves checked: before dispatch, a STANDARD agent verifies the spec is internally consistent and every task has a testable done-condition. A boss spec that fails this check gets fixed before any worker spawns.

**The boss is the least-checked agent in the run** — and across observed runs it authored a comparable share of defects to the workers. Non-negotiable, full list + evidence in `references/boss-discipline.md`: execute a correction against a real substrate before sending it (L24); re-run any command that gates a merge rather than trusting a pasted output, and never name the output you expect (L23); never `git add -A` while agents are live (L25); remove every container/process you start and keep an agent roster reconciled each round (L26); commit the observation, never the attribution (L33); record what you did, never what you concluded exists (L34); toolchain preflight before dispatch (L28).

**Workers** (ECONOMY/STANDARD per §3). Each receives exactly one task card (§6) + the constitution. A worker's "done" is a **claim**, never a fact.

**Skeptic** (STANDARD or FRONTIER; exactly one per run). Spawned after all tasks pass their checkers, before the boss declares done. Its brief is pure refutation: assume the build is broken and prove it — attack the assembled whole (integration seams between tasks, the gaming patterns in §9, constitution clauses nobody's checker owned, the checks themselves). It gets the constitution and the checkers' verdicts, and is scored on finding real breaks, not on agreeing. **Its brief names the BOSS-OWNED files as target one (L43)** — the shared files the boss took over to remove contention (L33) are the ones no lane's card names and therefore no lane's checker attacks; in one run all three lanes passed while five defects, two CRITICAL, sat in the boss's wiring. Brief it to attack BY CONSTRUCTION rather than by review, and to audit the self-tests' **coverage** — *which evasions does this suite not attempt?* A suite written by the tool's author tests the failures the author imagined. **It reports to the boss and only to the boss** — it never messages workers, never dispatches fixes, and never declares the run done itself. The boss adjudicates each finding (a skeptic can be wrong too; the §7 dispute path and rubric-amendment rule apply to its findings exactly as to a checker's), then routes accepted findings into the owning task's loop as feedback. Findings the boss rejects are recorded with the reason, not silently dropped. Distinct from checkers: checkers verify one task's done-condition; the skeptic hunts what no single done-condition covers.

**Checkers** (independent, decorrelated). Vocabulary from solution-tournament's ladder: prefer **CROSS-TIER** (a different Claude band via the model override), fall back to **SAME-MODEL** and label it honestly in the run log. Checkers **execute**:
- Code: run the build, run the tests, run the linter — read exit codes, not diffs.
- Web: fetch the URL, render the page (webapp-testing / browse skills), test both themes.
- Content: character-compare protected text against the source, refetch cited URLs.
- **Falsify the suite before trusting it (L8).** When a task's evidence is "the tests pass", the checker breaks the implementation on purpose, reruns, and reports how many tests still passed — then PROVES THE MUTATION LANDED (hash/diff the file after editing, before running — a never-applied mutant and a survived mutant are indistinguishable in test output, L13), and afterwards restores and proves byte-identity with a CONTENT HASH (`shasum` before vs after) — `git diff` is empty by construction for untracked files, so it proves nothing about new code (L12). A suite that passes on knowingly-broken code is measuring something other than its names claim. **The boss's mutation list is a coverage ceiling like its test list (L29) — tell the checker to ADD its own mutants**; a self-added one found a second survivor the boss had not thought of. When the output is a composite (`${label}:${computed}`), mutate the COMPUTATION while preserving the format — a difference-assertion is satisfied by the label alone and never reaches the computed part (L16). **And beware your own probe (L45): if the bug vanishes once you instrument it, bisect the probe's latency before believing it — twice in one run a debug query and a polling loop each WERE the fix. Assert on the system's own state, never on the flag the code under test sets.** **A survivor is not automatically a gap (L46)**: check for an either-sufficient sibling guard and try removing BOTH before recording a hole — deleting the "dead" one is the wrong fix, and the redundancy belongs in a comment. Watch especially for properties the subject *re-establishes on every call* (a context setter, a timeout, a cache warm) or SUPPRESSES once torn down (a state callback silenced after close): those can only be falsified from OUTSIDE the subject, so a test that goes through it will pass no matter what.
- **Assert the check examined something (L9).** Exit 0 means "this process reported no violation", never "no violation exists". Every check declares what it must have found — files linted, tests collected, tables discovered, fixtures loaded — and FAILS at zero, independently of exit code. Eight observed instances: a linter that opened no file in 197ms, security steps run against an empty database while 177 real violations existed, a policy runner printing `0 tests`. **A guard written from the examples already seen generalises to those examples, not to the class.**
- **Execute against inputs the worker did not author (L20).** An agent that writes both a transformer and its fixture encodes the same wrong assumption twice; they confirm each other perfectly and the suite goes green while the transformer matches nothing real. Allow-fixtures are GENERATED by the exact tool the exit criterion invokes, in the exact mode, committed with URL + date + checksum; deny-cases MUTATE ONE FIELD of a real fixture. "From the real producer" is not precise enough — a format with two real producers fails identically to a fake one.
- **Reversible operations are asserted on both sides (L36)** — state before and after, never the reversal's exit code. A no-op `down` migration produces exactly the same exit codes as a working one.
- **Treat "the check is a grep / regex / LIKE / substring" as a defect smell (L27)**, and ask what it does against the same content re-cased, restructured, concatenated, or moved one scope outward. One adversarial pass ran 20 constructed attacks and got past a security gate 8 times; every hard defect traced to text matching standing in for a semantic/AST/catalog check.
- A checker that only read the diff and agreed has failed its job. Verdicts are structured: `{verdict, evidence[], repro_command, feedback}`.

## 5. The constitution

Before any dispatch, the boss writes a one-page done-right standard for THIS build: stack conventions, quality floor (a11y/security/test coverage), forbidden shortcuts, and the exact verification command per task type. Derive it from CLAUDE.md + the repo; ask the user only what is underivable, in one batched round. Template: `references/constitution-template.md`.

Every worker and checker prompt embeds the constitution. Checkers grade against it, not vibes. Per-task instructions shrink to "task card + constitution". When a checker is proven wrong (§7), the fix is a constitution amendment, so the whole fleet learns.

## 6. Dispatch mechanics — every spawn is fully spec'd

**Baseline preflight (L55, before any spawn)**: never a type whose tool list is `*` or "all tools except…" (`general-purpose`, `Explore`, `Plan`): the MCP catalogue is ~74K tokens (run 16: general-purpose 165K and Explore 164K first turn vs `tdd-guide` 90K; 3 of 4 died). Use only types with a short explicit tool list (`tdd-guide`, `build-error-resolver`, `code-reviewer`, `typescript-reviewer`, `code-explorer`). Then `wc -c` the injected CLAUDE.md files and rules; ÷4 over half the band's window → shrink those files, never re-card.

**Toolchain preflight (L28, before any spawn)**: enumerate every binary named in the goals' exit criteria (`terraform`, `conftest`, `docker`, `psql`, `k6`, `gh`, validators) and start all installs in parallel FIRST. Acquisition is on the critical path and does not parallelize with itself; installing reactively costs a round-trip per discovery, and a fan-out that finishes authorship in 25 minutes then queues behind one serial download bought nothing. When a capability has two acquisition paths of very different sizes, start both. Verify the binary exists — do not trust the installer's exit code.

**Tool choice**: Agent tool for ≤4 tasks or when the user should review between rounds (explicit `model:` on every call — never inherit silently). Workflow tool for 5+ tasks, retry loops, or budget enforcement; the user invoking this skill is the required orchestration opt-in. **If the Workflow tool is not available, run the Agent-tool path in batches — that is the documented fallback, not a degradation.** A **round** = one batch of workers dispatched together, closed when every member has a checker verdict (or is declared dead) and the boss has reconciled the roster. Cap concurrent spawns at **~6** — agents spawn their own children, and an oversubscribed fleet stalls (observed; also the machine's CPU/RAM serves the checkers' builds).

**No bare instructions.** Every worker spawn carries a boss-authored **task card**:
- Objective (one sentence) · Inputs (inline extracts, per the context budget below) · Done-condition (testable, from the spec) · Verification command the checker will run · Required output schema `{status, evidence, files_touched}` · The constitution.
- **Quote the exit command verbatim (L21)** — character for character from the goal, never a paraphrase into something that seems equivalent. `opa test` and `conftest test` differ in loader strictness; `vitest` and CI differ in env; `tsc -p` and `tsc -b` differ in project refs. A substitution is an unproven assumption, and it is the one a worker will inherit.
- **Never name the output you expect to see (L23)** — "you should get `(no results)`" is the output shape easiest to produce without doing the work. Ask for the command's raw output.
- **If every port implementation in the oracle is a fixture, no test can reach an error path (L44).** Fixtures return cleanly by construction, so the error boundary reads as covered and is untested. The boss's oracle ships one adapter that THROWS on purpose.
- **The card's test list is the coverage ceiling (L29).** A worker will not invent the case you omitted, so a boss-authored enumeration is a load-bearing artifact — review it for completeness before dispatch, not after. One omitted case ("enabled but with no policy at all") was exactly where the tool had a permanently dead branch.
- **When the card assigns a reading that answers a specific question, say so** — "the endpoint you are about to research is in Appendix A" beats "also read Appendix A". A worker treated a named document as background and burned a full research segment rediscovering one line of it.
- **Frame inherited code as suspect (L30, CANDIDATE)**: say it is an untested draft by someone else, that finding its bugs counts as success, and that the report must state where it looked and found NOTHING — separately from what it fixed. The most reliable observed reports all came from cards written this way.

**Context budget (hard rule — EVERY observed worker death traces to it, not to capability).** Full protocol, ceilings, pre-dispatch checklist, and death-diagnosis table: **`references/context-budget.md` — that file is the source of truth; this list is only the index**. Five causes: reading list over 2 files/50-line extracts (L1) · unredirected command output — the larger channel (L18: redirection is the FIRST line of every card) · two capabilities bundled in one card (L17: the boss ships the working test harness; the worker's card is "make these tests pass") · retry transcript accumulation (L41, CANDIDATE: retry 2+ respawns fresh) · **the SUBJECT itself is over budget (L54)** — a compliant card still kills the worker when the file it must EDIT or the suite it must RUN is huge; four thrash deaths in one day came this way. Measure the write target and the suite with `wc -l` before dispatch, not just the reading list. Card size stays constant across bands (L3) or the run is uninterpretable. Run every card through the context-budget.md checklist before spawning; total payload ~200 lines. **Never escalate a band for a context death** — re-card SMALLER at the same band, after checking the filesystem for salvage (L4).

**Verification scope (shared-tree safety):**
- Worker/checker verification is narrow: single-file test run (e.g. `vitest run <file>`) + typecheck (`tsc --noEmit`). **The full build is boss-only, once, after all workers finish** — two concurrent full builds against one working tree corrupt build artifacts (`.next` ENOENT) and produce false FAILs that look like the worker's fault. The only exception: each worker has its own git worktree.

Checkers get the matching card plus the worker's claim — never the worker's reasoning (that would correlate their errors).

Prefer existing specialized agents via `subagent_type` + model override (e.g. `typescript-reviewer` as a STANDARD checker) over generic agents. **Isolation default**: workers writing to disjoint, exclusively-owned paths share the tree (cheap, and it held across the observed runs); any two workers whose writes could touch the same path get worktrees — when in doubt, worktree. The Workflow snippet worktrees unconditionally; that is the safe default for 5+ tasks, not a contradiction. Copy-paste call shapes for both tools: `references/call-shapes.md`.

**Communication contract (both directions, during the build):**
- Every worker/checker/skeptic prompt ends with the reporting clause: on completion, SendMessage your result JSON to `main` — an idle notification without the JSON is an incomplete report. If a spawned agent goes idle without delivering, the boss requests the result by name once before considering the task stalled.
- **Assume the report may never arrive.** Dead agents can leave no discoverable transcript and ignore pings — and name-based result lookup is known-broken on this machine. Recovery ladder (per `~/.claude/rules/common/subagent-report-delivery.md`): (1) the filesystem — `git status` / expected outputs ARE the report; (2) TaskOutput with the RAW agent id from the spawn result; (3) mechanical transcript harvest: `python3 ~/.claude/scripts/harvest_agent_tail.py <agent-name> --session <session-dir>` — never read the full transcript; (4) only then one SendMessage nudge. And do not commit to a root cause for an agent failure until its idle notification lands — the real reason (e.g. autocompact thrash) often arrives late and out of band, after a plausible-but-wrong diagnosis.
- **Worker → boss, mid-task**: workers are told to SendMessage `main` immediately when blocked, when the spec is ambiguous, or when two constitution clauses conflict — and to STOP rather than guess. A question costs one message; a guessed-wrong implementation costs a full retry loop.
- **Boss → worker, mid-task**: the boss pushes spec corrections and constitution amendments to affected named workers via SendMessage as soon as they're ratified — workers must not learn about an amendment from a FAIL verdict.
- Spawn workers with `name:` so they stay addressable for retries, amendments, and disputes; keep all coordination through the boss (workers never message each other — sibling chatter correlates errors and bypasses arbitration).

## 7. Verification loop

Per task: worker → checker executes → **PASS** (evidence attached) or **FAIL** (specific and reproducible: command run, expected, actual) → retry. **Retry 1**: same worker, feedback appended. **Retry 2**: FRESH respawn, same band, boss-rewritten card that inlines the specific fix (L41 — the old transcript already holds the failed attempt and its output). Still failing → escalate the band once for **one** attempt (a fresh spawn, briefed with both failures) → then boss arbitrates. Total: 3 worker attempts at band + 1 escalated, then the boss.

**When a tightened check starts failing things that used to pass (L10)**, each failure is evidence about the OLD check before it is noise about the new one. Ask why the old check passed it. Loosening on the first false positive discards exactly the finding the tightening was for.

**A `blocked` report gets the same review as a `done` report (L22)** — the opposite of the instinct to file it as "not the worker's fault". Blocked must be scoped to the step the missing dependency touches, with an explicit per-done-condition list of what was and was not finished. **When the blocker is on the VERIFICATION step, stop accepting fixes to that file entirely** rather than accumulating unverifiable edits: one file took three rounds of "FIXED" with zero executions, and two of its five defects were introduced BY fixes. Remove the incentive too — tell the worker that `blocked_on: no way to execute` plus a list of unproven assertions will be accepted immediately.

**The boss re-runs any command that gates a merge (L23).** §4 requires checkers to execute; the same applies here, because a checker can be fed the same false report. A pasted `(no results)` once described three live hits in the four tests that verified tenant isolation.

**Guardrails can be mutually unsatisfiable (L37).** When two frozen rules cannot both hold, BLOCKED is the correct output and an agent that "just makes it pass" necessarily breaks something real — in one case the obvious fix would have greened the check while creating exactly the regression the other rule exists to prevent, so the tool would have certified the damage. The boss resolves by amendment, never by the convenient reading.

**Disputes**: a worker may contest a verdict. The boss arbitrates with both outputs in hand. If the checker was wrong, amend the checker's rubric in the constitution — don't just flip the verdict. Verification runs in both directions: boss outputs pass through a checker too, and rank exempts nobody.

**Stop condition**: 3 boss arbitrations on the same task → stop and surface to the user with both sides. Never loop past that.

**Final gate**: when every task has PASSed, the skeptic (§4) runs against the assembled build and reports to the boss. **Freeze the tree while it runs** — do not dispatch fixes into the same working tree mid-audit, or give the skeptic its own worktree pinned to the commit under test; otherwise a worker's in-flight mutant reads as shipping code and a landed fix reads as a false positive (L14). The boss adjudicates, routes accepted findings into the owning task's loop as feedback, and re-runs the skeptic on the fixed build — briefing it on what changed and on any new risk the fix introduces (a guard added to stop one failure is a prime suspect for swallowing a legitimate case). Re-runs also re-verify that the fix's own tests actually fail against deliberately broken code, or the coverage is a mirage. Only the boss declares done, and only on a skeptic pass with executed attacks logged.

## 8. Cost accounting

End every run with a table: tasks per band, concrete models used, retries, escalations, and estimated spend vs an all-FRONTIER baseline (prices from `references/model-intel.md`). The user should see whether the cheap bands actually carried the load.

**Judge a run by delivered artifacts per token, not by agents spawned.** Agents that die produce zero artifacts but still dominate spend; a run where two ECONOMY workers delivered and three STANDARD agents burned tokens dying is an ECONOMY win and a card-writing failure, not a tier finding.

## 9. Failure modes

| Symptom | Response |
|---|---|
| Checker fails constitution-compliant work repeatedly | Dispute path (§7); amend rubric |
| Worker games the check: hidden text, hardcoded expected values, skipped/disabled tests | Checkers verify *mechanism*, not just output — grep for `skip`/`display:none`/hardcoded fixtures; the check checks the check |
| Correlated errors (worker and checker share priors) | Prefer CROSS-TIER checkers; never let a worker's same-band sibling check the same task it could have written |
| Repeated thrash deaths in one repo on cards that pass the checklist (L54) | The SUBJECT is over budget, not the card. Boss extracts a small module for the lane to own; if extraction is unsafe, the lane becomes a boss lane. Never respawn the same lane at any band |
| Worker dies of context exhaustion / autocompact thrash | The card violated the context budget — re-card smaller, same band, never escalate. **Full diagnosis table (context vs bundling vs infra flake): `context-budget.md`** — this row is the reminder, not the procedure |
| False FAILs with corrupted build artifacts (`.next` ENOENT etc.) during parallel work | Concurrent full builds in one working tree — infrastructure fault, not the worker's. Scope worker verification per §6; boss runs the one full build after |
| Agent goes silent; no report, no transcript | Check the filesystem (`git status`, expected outputs) for the work itself; salvage partial intel from what landed. Withhold root-cause judgment until the idle notification arrives. **Absence of artifacts means the work is not done — NOT that the agent is dead, and NOT that anything was lost if you take the card over.** Record the target file's hash and mtime in the takeover note so a later "you overwrote me" claim is settled by evidence rather than apology (L4b) |
| A late pipeline step goes red the first time it is ever reached (L11) | Not a regression from the change that reached it. Fail-fast ordering hides the tail indefinitely, so the steps furthest from step 1 are the likeliest to be broken. Triage as findings and budget for them |
| A check passes but you cannot say what it examined (L9) | Vacuous pass. Make the examined-count part of the step and fail at zero. `197ms` is not a passing lint; it is a step that never opened a file |
| A safety rule flags its own definition or its own tests (L35) | Structural, not a bug. Scope the exception to NAMED PATHS with a reason each. "Tests are exempt" would have disabled three security rules across the repo forever |
| A grep-based check fails on a comment explaining the rule (L39) | A text match cannot tell code from prose about code. Scope to executable positions (YAML `run:` keys, AST call sites) or say so in the check's header — otherwise it pressures maintainers to delete the comment instead of fixing the code. Also: fixture identifiers must not be substrings of one another |
| A fix landed but production still broken (L32) | The fact lives in two artifacts and only one was fixed. Verify through the path PRODUCTION uses; a decision recorded in an ADR is upstream of the diff. That agreement needs its own mechanical check |
| Coordination messages exceed implementation work | Collapse to in-session execution, tell the user, and log why |

## 10. Self-improvement loop (mandatory — the run is not done until the retro is written)

The skill maintains itself the same way it treats a build: evidence, execution, amendment. Protocol details and templates: `references/run-retro.md`. Ledgers: `references/lessons.md` (compact index — the pre-run read), `references/lessons-evidence.md` (full evidence; read only when judging a promotion/demotion), `references/boss-discipline.md` (boss-side rules in operational form), + a repo-local `foreman-notes.md` when one exists.

**Pre-run (boss, before writing the spec) — this list is authoritative; no other section adds to it:**
1. `references/lessons.md` (~70 lines — the index; open `lessons-evidence.md` only to judge a promotion).
2. `references/boss-discipline.md` + `references/context-budget.md` (~320 lines — the two operational references).
3. The repo's `foreman-notes.md` if present. **If absent, the boss creates it at post-run** with build commands, shared-tree hazards, and parallelization-safety notes discovered this run.
Total mandatory pre-run read ≈ 600 lines including this file — proportionate for a FRONTIER boss, and capped by §10's size limits so it stays that way. Any ACTIVE lesson matching this job's shape gets applied to the cards/constitution — a documented fix that isn't applied is a known bug shipped on purpose.

**Mid-run (self-healing):**
- When a symptom matches a §9 row or an ACTIVE lesson, apply the documented response immediately — do not re-diagnose from scratch. Log in the run notes whether the documented fix actually worked; a fix that failed is itself a finding.

**Post-run (boss, after the cost table):**
1. Append a run section to the ledger(s): outcome table per agent, what worked, what failed, confounds explicitly named, artifacts-per-token verdict, and a **death table** — every agent that died, its card size in lines, its reading-list length, whether its commands were redirected, its retry depth, and the cause class (context / bundling / infra flake / unknown). Context deaths are the skill's most expensive failure and the only way the loop learns about them is if they are counted.
2. Diff the run's lessons against the current skill files. Promotion rule:
   - Seen once → record as CANDIDATE in `lessons.md` with the evidence.
   - Confirmed twice across runs, OR seen once with an airtight causal chain (all failures share one cause, mechanism understood) → promote: edit SKILL.md / the references directly, date-stamped, and mark the lesson PROMOTED with a pointer to where it landed.
   - Contradicted by later evidence → mark DEMOTED with the counter-evidence; revert the promoted edit. Never silently delete.
3. **Guardrails on self-edits** (a self-improving skill's failure mode is self-lobotomy):
   - Never weaken or remove a verification/safety rule (execute-don't-read, checker independence, context budget, build scoping) — those only tighten, or go through the user.
   - Every new rule must name the run(s) that earned it. No speculative rules.
   - Negative-test new checks: a new "checker must grep for X" rule ships with one example that would have FAILed under it.
   - **Promotion edits are themselves checked**: before committing, a STANDARD agent reviews the diff against these guardrails and run-retro.md's airtight-chain checklist. The boss is the least-checked agent in the run (§4) — that applies to its memory edits too.
   - Size caps (the context budget applies to the skill itself): SKILL.md ≤200, `lessons.md` ≤120 and `boss-discipline.md` ≤250 (both read pre-run), other references ≤250. `lessons-evidence.md` is exempt from the pre-run budget but capped at 450. At a cap, compress or move evidence out of the read path — never drop a lesson.
   - Named confounds stay named until a controlled run settles them (e.g. band vs card size) — a confound never quietly becomes a conclusion.

**Close-out (the run is not done until these have run).** The loop is worthless if its memory is not durable — `lessons.md` and `run-retro.md` sat untracked in git for the skill's entire history, so every lesson was one machine failure from being lost:
```
python3 ~/.claude/skills/foreman/tools/lint.py   # caps, ID sync, landed-in, template, refs — MUST exit 0
git -C ~/.claude add skills/foreman && git -C ~/.claude status --short skills/foreman
git -C ~/.claude commit -m "docs(foreman): run <n> retro — <one-line outcome>" && git -C ~/.claude push
```
Gate the commit on the linter's exit code (`&&` after it, or an explicit if) — a newline instead of a guard once pushed a cap breach straight past a failed check.
A promotion edit that is not committed is a lesson learned and thrown away.

## Related skills

- **agentic-engineering** — the advisory tier-mapping doctrine this skill operationalizes
- **solution-tournament** — competing-solution scoring; source of the checker-decorrelation ladder
- **agent-workflow-designer** — bespoke workflow shapes beyond boss/worker/checker
- **verification-loop** — single-task verification when no org chart is needed
- **webapp-testing** / **browse** — checker execution surfaces for web builds
- **llm-cost-optimizer** — auditing spend after the fact
