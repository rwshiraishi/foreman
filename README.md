# Foreman

**A boss/worker/checker pattern for AI coding agents.** One expensive model writes the spec and inspects the work but never touches the code. Cheap models do all the building. Every task is verified by an independent agent that *runs* the thing instead of trusting the builder's report. An adversarial skeptic attacks the finished build before anyone calls it done.

The result is a run that costs a fraction of an all-frontier build and catches defects that self-review never finds.

Every report routes to the boss. Nothing is declared done by the agent that did the work.

```
                    ┌──────────────────────────────────────────┐
      task cards    │  BOSS  (frontier tier)                   │   claims · blockers
      amendments  ┌─┤  spec · constitution · adjudication       ├─┐ verdicts · findings
      retry       │ │  never writes implementation code         │ │ disputes
      feedback    │ │  the only role that declares DONE         │ │
                  │ └──────────────────────────────────────────┘ │
                  ▼                                              │
        ┌─────────────────┐                                      │
        │  WORKERS        │ ── claim (a claim, not a fact) ──┐    │
        │  cheap tier     │                                  │    │
        │  one card each  │                                  ▼    │
        └─────────────────┘                        ┌─────────────────┐
                  ▲                                │  CHECKERS       │
                  └── retry w/ specific feedback ──┤  run the build  │
                         (routed by the boss)      │  drive the UI   │
                                                   │  1 per task     │
                                                   └─────────────────┘
                  ┌─────────────────┐                       │
                  │  SKEPTIC        │  findings ────────────┘ all PASS
                  │  attacks the    │  ▲  (boss spawns the skeptic,
                  │  assembled whole│──┘   adjudicates, may reopen a
                  │  1 per round    │      task loop, then re-runs it)
                  └─────────────────┘
```

Workers never message each other. Checkers never message workers. The skeptic reports to the boss and only to the boss — it cannot dispatch its own fixes, and it cannot end the run.

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

Foreman is a skill: a markdown file plus three reference documents. There is nothing to build and no dependencies.

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
    call-shapes.md                  copy-paste dispatch: task cards, workers, checkers, skeptic, comms
    constitution-template.md        the done-right standard, with a worked example
    model-intel.md                  model → band/price/strengths, date-stamped and refreshable
commands/
  model-route.md                    optional Claude Code slash command front door
adapters/
  codex-foreman.md                  Codex CLI prompt adaptation
```

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
