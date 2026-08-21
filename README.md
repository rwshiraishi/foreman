# Foreman

**A boss/worker/checker pattern for AI coding agents.** One expensive model writes the spec and inspects the work but never touches the code. Cheap models do all the building. Every task is verified by an independent agent that *runs* the thing instead of trusting the builder's report. An adversarial skeptic attacks the finished build before anyone calls it done.

The result is a run that costs a fraction of an all-frontier build and catches defects that self-review never finds.

Every report routes to the boss. Nothing is declared done by the agent that did the work.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="diagrams/orgchart-dark.png">
  <img alt="Boss at the top sends task cards and retries to workers and card-plus-claim to checkers, and spawns the skeptic once all tasks pass. Workers send claims, checkers send verdicts, and the skeptic sends findings — all back to the boss." src="diagrams/orgchart-light.png" width="820">
</picture>

Every arrow ends at the boss. Workers never message each other, checkers never message workers, and the skeptic reports to the boss alone — it cannot dispatch its own fixes and it cannot end the run.

## Why this exists

Two problems collide when you give a coding agent a real job.

**Cost.** Frontier models are 5-10x the price of small ones. Most of a build is not frontier work: writing markup, wiring a form, adjusting config. Paying top rate for boilerplate is an org design mistake, not a model limitation.

**Trust.** An agent that reports "done, tests passing" is making a claim, not stating a fact. It may have hidden text to satisfy a content check, hardcoded a value to satisfy an assertion, or written unit tests that pass while the shipped feature is broken. Reading the diff and nodding does not catch this. Running the thing does.

Foreman answers both with structure rather than with a better model: expensive judgment at the top, cheap labor in the middle, and independent execution-based verification that nobody, including the boss, is exempt from.

## How it works

**1. Discover the models, don't hardcode them.** At run start Foreman inspects what's actually dispatchable in the session, consults a cached intel table of prices and capabilities, and refreshes that table by research when it's stale. Models map to three bands — FRONTIER, STANDARD, ECONOMY — and all the routing logic speaks in bands. A new model release updates one table, not the skill.

**2. The boss writes a constitution first.** Before any work is dispatched, one page defines what "done right" means for this build: stack conventions, quality floor, protected content, forbidden shortcuts, and the exact command that verifies each task type. Every worker and every checker gets it. Checkers grade against the constitution, not against taste. This replaces task-by-task micromanagement with a standard enforced on every round.

**3. Task cards, never bare instructions.** Each worker gets exactly one card: objective, exact input paths, a testable done-condition, the verification command that will be run against it, the required output schema, and the constitution. Ambiguity is the boss's fault, and the boss's spec is itself checked before dispatch.

**4. Checkers execute.** A checker runs the build and reads exit codes, fetches the page and renders it, character-compares protected text, drives the UI in a real browser. It receives the worker's claim but never the worker's reasoning — shared reasoning correlates errors. Checkers prefer to be a different tier than the worker they check. A checker that only read the diff and agreed has failed its job.

**5. Failure is specific, and rank doesn't protect you.** A FAIL comes back with the command run, what was expected, and what was observed. The same worker retries with that feedback. Workers can dispute a verdict and the boss arbitrates with both sides in hand — and when the checker was wrong, the constitution's rubric gets amended so the whole fleet learns. The boss's own output goes through a checker too.

**6. A skeptic attacks the assembled build.** After every task passes, one adversarial agent assumes the build is broken and tries to prove it: integration seams no single task owned, gaming patterns, constitution clauses nobody's checker covered, and the quality of the checks themselves. It's scored on real breaks found, not on agreement.

## What it caught on its first live run

A three-task static site build (markup, stylesheet, form validation) with a protected quote that had to ship verbatim:

| Rung | What was caught |
|---|---|
| **The boss** | The spec checker found the task cards never required the ids and classes the other tasks depended on — each task could pass alone while the assembled site broke. Caught before any worker spawned. |
| **A worker** | The form JS reported "done, 7/7 tests passing" and its unit tests genuinely passed. The browser-driving checker found three integration defects: a phantom success box visible on page load, error boxes that never visually cleared (a CSS `display:flex` rule silently overriding the `hidden` attribute), and native `required` validation blocking the submit handler entirely. |
| **The checkers** | All three tasks passed verification. Then the skeptic broke it anyway: clicking submit a second time after success wiped the confirmation and showed three false errors — deterministic at every delay tested. It also proved the worker's test file was a mirage: seven passing tests, zero DOM coverage of the shipped behavior. |

Nobody had to read a diff to find any of it.

## Install

Foreman is a skill: a markdown file, eight reference documents, and one self-lint script. There is nothing to build; the linter needs only Python 3.

### Claude Code

```bash
git clone https://github.com/rwshiraishi/foreman /tmp/foreman
mkdir -p ~/.claude/skills/foreman
cp -r /tmp/foreman/skill/* ~/.claude/skills/foreman/
cp /tmp/foreman/commands/model-route.md ~/.claude/commands/   # optional slash command
```

Project-scoped instead of global: use `.claude/skills/foreman/` inside the repo.

Invoke it by asking for it in plain language — "run the foreman on this build", "orchestrate this with cheap models for the easy parts" — or with `/model-route <task>` if you installed the command. Claude Code's Agent tool provides the `model` override the pattern needs, and the Workflow tool provides per-agent `model` and `effort` for larger fan-outs.

### OpenAI Codex CLI

Codex reads `AGENTS.md` from the project root and supports custom prompts in `~/.codex/prompts/`.

```bash
git clone https://github.com/rwshiraishi/foreman /tmp/foreman
mkdir -p ~/.codex/prompts
cp /tmp/foreman/adapters/codex-foreman.md ~/.codex/prompts/foreman.md
```

Then `/foreman <task description>` in a Codex session. For a project-wide default, append the contents of `skill/SKILL.md` to the repo's `AGENTS.md` under a `## Foreman orchestration` heading.

Codex spawns subagents differently than Claude Code and its model selection is per-session rather than per-agent, so the band mapping applies at the session level: run the boss session on a frontier model, and dispatch worker and checker sessions on cheaper ones. The verification discipline — checkers execute, claims are not facts, a skeptic attacks the whole — transfers unchanged.

### Cursor, Windsurf, and other rules-based agents

```bash
cp /tmp/foreman/skill/SKILL.md .cursor/rules/foreman.mdc     # Cursor
cp /tmp/foreman/skill/SKILL.md .windsurf/rules/foreman.md    # Windsurf
```

Add the `references/` files alongside if your tool supports on-demand file reads; otherwise the main file stands alone.

### Any agent that reads a prompt

The pattern is prompt-level, not tool-level. Paste `skill/SKILL.md` into a system prompt or project instructions. The only hard requirements are the ability to run more than one agent and the ability to execute commands for verification. Everything else is discipline.

## Repository layout

```
skill/
  SKILL.md                          the pattern — org chart, bands, loop, failure modes
  references/
    context-budget.md               the #1 killer: every observed worker death, and how to prevent it
    boss-discipline.md              boss-side rules — the boss is the least-checked agent in the run
    call-shapes.md                  copy-paste dispatch: task cards, workers, checkers, skeptic, comms
    constitution-template.md        the done-right standard, with a worked example
    model-intel.md                  model → band/price/strengths, date-stamped and refreshable
    lessons.md                      the ledger index: one line of law per lesson (read every run)
    lessons-evidence.md             full evidence, mechanisms, negative tests (read only to judge a promotion)
    run-retro.md                    mandatory post-run retro protocol and self-edit guardrails
  tools/
    lint.py                         self-lint: size caps, lesson-ID sync, template rules, broken refs
commands/
  model-route.md                    optional Claude Code slash command front door
adapters/
  codex-foreman.md                  Codex CLI prompt adaptation
```

The ledger is split deliberately. `lessons.md` is the pre-run read and stays under 120 lines no
matter how many lessons accumulate; the evidence that justifies each one lives in
`lessons-evidence.md` and is opened only when a promotion or demotion is being judged. A skill
that lectures workers about context budgets should not hand its own boss a 400-line preamble.

## The skill maintains itself

Foreman treats its own doctrine the way it treats a build: evidence, execution, amendment. Every run ends with a mandatory retro. Lessons live in `skill/references/lessons.md` with a lifecycle — seen once is a CANDIDATE, confirmed twice (or once with an airtight causal chain) gets promoted into the skill files with a date stamp, contradicted later gets demoted with the counter-evidence recorded. Nothing is silently deleted, and open questions stay listed as UNANSWERED until a run is designed to settle them.

"Airtight" is a checklist, not a feeling: the mechanism fits in one sentence, it is independent of the repo and language, a negative test exists (the concrete example that *would* have shipped under the old practice), and no named confound offers a competing explanation. Fewer than four and it stays a CANDIDATE.

**The loop is enforced by a machine, not a promise.** `skill/tools/lint.py` checks size caps, lesson-ID sync between the index and the evidence file, duplicate IDs, promoted rules that never name where they landed, the task-card template's own first-line rule, and broken cross-references — and every check reports how many things it examined and fails at zero, obeying the rule it enforces. The retro close-out chains the commit behind its exit code. This is not decoration: an earlier close-out used a newline instead of a guard and pushed a cap breach straight past a failing check.

**43 lessons and 4 open questions are currently on the books.** A sample of what the runs actually taught:

| | |
|---|---|
| **Nothing distinguishes "clean" from "nothing to check"** | Eight separate instances of a green check that examined zero things: a linter that opened no file in 197ms, security checks run against an empty database while 177 real violations existed, a policy runner reporting `0 tests` and exit 0. Exit 0 means "no violation was reported", never "no violation exists". |
| **The co-authored-fixture trap** | When an agent writes both a transformer and its test fixture, both encode the same wrong assumption and confirm each other perfectly. A 26/26 green policy suite protected infrastructure whose rules could not fire at all — and the "fix" that made the suite green moved the code *away* from correctness. Fixtures must be generated by the exact tool the exit criterion invokes, in the exact mode it invokes it. |
| **A `blocked` status is not a safe status** | Three reports in one run used a genuine environment blocker as a wrapper carrying unrelated unfinished work. Worse: when the blocker sits on the *verification* step, every later edit silently becomes an unproven claim. One security file took three rounds of "FIXED" with zero executions, and two of its five defects were introduced by fixes. |
| **The boss is the least-checked agent** | It authored a comparable share of defects to the workers: a wildcard `git add` three times (once committing 240MB of provider binaries), two corrections sent to workers without ever being executed, leftover verification containers that starved a worker for a full segment, and an `ls` of six empty directories read as proof the files existed. That earned its own reference file. |
| **Every worker death was context, not capability** | Across five runs, not one death was a model that could not do the task. Three causes: reading lists that pointed at large files, unredirected command output (the larger channel, and the one a file cap does not cover), and cards that bundled implementation with harness debugging. Escalating the band for a context death is the common wrong response — a bigger model on the same card dies the same way and costs more. |

The ledger also records the skill's own misses. Its lesson files sat **untracked in git for the skill's entire history** — no ignore rule caused it, and no step in the loop said to save them — so every lesson was one machine failure from being lost. That is now L40, and the close-out ends by pushing.

## Design notes

**Bands, not model names.** Every routing decision names a band. Concrete models appear in exactly two places: the intel table and the end-of-run cost report. This is what keeps the skill from rotting the week a new model ships.

**Cheap workers are a bet you can afford.** The pattern assumes cheap models cut corners and prices that in. It does not depend on their honesty; it depends on the checks. That's why the answer to "who checks the checkers" is the skeptic, and the answer to "who checks the boss" is a spec check before dispatch.

**Decorrelation over redundancy.** Two agents from the same model with the same context tend to make the same mistake and agree confidently. Checkers get the claim without the reasoning, prefer a different tier than the worker, and the skeptic is briefed to refute rather than confirm.

**Constitution over instructions.** Naming the standard once and enforcing it every round scales; restating requirements per task does not, and drifts.

**Know when not to use it.** If the job fits in two files and under a hundred lines, orchestration costs more than the work. Foreman says so in its own first section.

## Prior art and credit

The org-chart-plus-verification framing was popularized in a widely shared demonstration of rebuilding an author's website with a tiered agent team. The checker-decorrelation vocabulary (cross-vendor, cross-tier, same-model) is borrowed from a solution-tournament pattern for scoring competing implementations. The idea that verification must execute rather than read is older than any of it and keeps having to be relearned.

## License

MIT. See [LICENSE](LICENSE).
