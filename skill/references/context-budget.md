# Context budget — the run's #1 killer

**Every observed worker death in this skill's history traces to context, not capability.**
Across five runs: 3 deaths in run 1 (marketing port), 2 in run 3 (Sentinel G-1.4), 1 in
Sentinel run 1 (`w2-infra`, "Prompt is too long · automatic compaction failed"), plus the
user-reported recurrences that promoted L17 and L18. Not one was a model that could not do
the task. Escalating the band for a context death makes it worse — a bigger model on the
same card dies the same way and costs more.

**A dead worker delivers zero artifacts and still bills for everything it read.** Under the
artifacts-per-token metric (L5), context deaths are the single most expensive failure the
skill has.

## The four causes, in observed order of frequency

### 0. The fixed baseline is already most of the window (L55, run 16)
Every subagent loads the global CLAUDE.md, every `~/.claude/rules/**` file, the project
CLAUDE.md and the tool catalogue BEFORE it reads its card. Measured 2026-09-01 (Sentinel):
sonnet workers' first turn was 163,898 input tokens of a 200K window; the project CLAUDE.md
was 131 KB, 95 KB of it a §7 that its own header says must be ten lines. Both sonnet
workers hit 6 compaction markers and died on 40-line cards with ≤2 reads; the haiku worker
(119K start) delivered. No card discipline survives an 82% baseline. **The largest single
weight is the agent TYPE's tool catalogue**: the skeptic respawned as `tdd-guide` (five tools)
started at 90,536 tokens against 164,936 for `general-purpose` (every tool + every MCP) with
an identical brief — 74K tokens bought by one parameter. `Explore` measured 164K too: any type
whose tools are `*` or "all except…" carries the whole MCP catalogue. Dispatch only types with a
short explicit tool list. **Preflight**: sum the
bytes of the injected files (`wc -c` on the CLAUDE.md files + rules dir), divide by 4, and
if that exceeds half the worker's window, cut the injected files (move history out of
CLAUDE.md into `docs/`) before any spawn. Re-measure from the transcript's first `usage`.

### 1. Reading list too long (L1)
Card names 8-10 files; the worker dutifully reads them all. Run 1: 3 of 3 deaths had 8-10
file cards, both survivors had ~3.
**Rule**: reading list ≤2 files + the constitution. Anything over ~50 lines is EXCERPTED BY
THE BOSS into the card. The boss's real advantage is knowing which 30 lines matter — spend
it at card-writing time, not by pointing a worker at a 340-line file.

### 2. Command output flooding (L18)
The bigger channel, and NOT covered by rule 1. A card can obey the file cap perfectly and
still kill the worker by telling it to run something loud. `psql` loading a 1200-line schema
emits a NOTICE per object; installs stream progress; a full test run prints every case;
`terraform init` and `docker pull` are worse.
**Rule**: output redirection is the FIRST line of every card, not a footnote.
```
cmd > /tmp/o.txt 2>&1; tail -30 /tmp/o.txt      # and echo $? separately if it matters
```
Ban outright in cards: bare `cat` of anything unbounded, `pnpm install` without redirect,
schema/migration loads without redirect, recursive `grep`/`find` across the repo without
`| head`.

### 3. Task bundling — two capabilities in one card (L17)
The card asks for "implement X" AND "get the test harness working". Harness debugging is
high-iteration and high-token: every failed boot prints a stack trace into context.
Run 3 G-1.4: the bundled card produced ZERO files in 33 minutes; a sibling checker with a
similar "boot Postgres yourself" card died outright. The boss then fixed the harness in ~10
minutes by copying an existing test file.
**Rule**: one capability per card. When the acceptance oracle needs non-trivial environment
setup, **the boss builds the harness and ships it working**; the worker's card is "make
these tests pass". Splitting a card is free; a dead worker is not.

### 4. Retry accumulation (CANDIDATE — inferred, not yet observed directly)
The §7 loop retries the SAME worker with feedback appended. Its context already holds the
first attempt, its file reads, and its command output; each retry adds more.
**Provisional rule**: retry 1 continues the same worker. **Retry 2+ respawns FRESH** with a
boss-rewritten card that inlines the specific fix needed, and does not inherit the failed
transcript. Marked CANDIDATE and labelled inferred because no run has yet been instrumented
to attribute a death to retry depth — do not treat it as settled. **Settle it** by logging
retry depth against death in the next run's retro.

### 5. The SUBJECT is over budget (L54)
The card is clean and the worker still dies. Causes 1-4 are all card-authoring failures;
this one is not. The file the worker must **edit**, or the suite it must **run**, is itself
too large — and neither is optional, so no amount of excerpting helps. A 800-line screen
file must be read to be patched; a Testcontainers suite prints a boot transcript on every
iteration. Sentinel run 14: four workers on ≤200-line redirected cards died of autocompact
thrash in one day, three with ZERO artifacts, every one of them assigned to a screen file
of 600-800 lines. Siblings on small pure modules (census math, config, single-function
fixes) delivered from identical card templates.

**Rule**: before dispatch, `wc -l` every file the worker will WRITE TO and every suite its
verification command runs. Over the write-target ceiling, do not dispatch the lane as-is.
Escalation ladder, in order:
1. **Excerpt-and-patch** — the card names exact anchor strings and the replacement text, and
   forbids reading the whole file. Works for narrow, well-located edits only.
2. **Extract first** — the BOSS pulls the sub-component into a new small file (a boss refactor,
   committed, tests green), and the worker owns that file. This is the preferred fix: it
   shrinks the subject permanently and every later lane on it is cheap.
3. **Boss lane** — the boss does it in-session, serially, with the same TDD + mutation
   discipline (L53). Last resort: it does not scale and it spends the scarcest agent.

**Never respawn the same lane at any band.** Band does not change the subject's size, and a
FRONTIER worker on an 800-line screen file dies the same way for more money.

Record the over-budget subjects in the repo's `foreman-notes.md` so the next run staffs
correctly instead of rediscovering it with three corpses.

## Ceilings (calibrated from observation, revise with evidence)

| Thing | Ceiling | Basis |
|---|---|---|
| Reading list | 2 files + constitution | L1, run 1 |
| Any single inline extract | ~50 lines | over this, excerpt harder or split the card |
| ALL inline extracts combined | ~80 lines | 2×50 does not fit: 100 of extract + ~25 template skeleton + a test enumeration blows the 120 card ceiling. Two sources means smaller excerpts each |
| Card body (excl. constitution) | ~120 lines | Sentinel run 1 cards ran 60-75 and survived |
| Constitution | ~80 lines / one page | it is embedded in EVERY spawn — its cost is multiplied by the fleet |
| Total spawn payload | ~200 lines | card + constitution, measured with `wc -l` |
| Injected baseline (agent-type tool catalogue + CLAUDE.md files + rules) | ≤ 50% of the worker's window at its first turn; never `general-purpose` (measured +74K) | L55, run 16: 164K/200K start killed 2 of 3 workers on compliant cards; measure with `wc -c` ÷ 4 before dispatch, confirm from the first `usage` in the transcript |
| Worker write-target file | ~400 lines | L54, run 14: 600-800-line screen files killed 4 of 4 workers assigned to them; small-module lanes from the same templates all delivered |
| Suite the worker must run | no container/server boot | L54 + U5: server-booting suites emit a large transcript per iteration that redirection does not fully contain |

These are working numbers from runs that survived, not measured limits. Treat a card at the
ceiling as a smell, not a pass.

## Pre-dispatch checklist (the boss runs this on EVERY card, before spawning)

1. `wc -l` the assembled payload. Over ~200 lines → split the task or excerpt harder.
2. Count files in the reading list. Over 2 → excerpt them inline instead.
3. Does the card ask for more than one capability? → split it.
4. Does every command in the card redirect its output? → if not, add it.
5. Does the card require booting/debugging an environment? → the boss builds that first.
6. Is the card size the same as its siblings' this round? (L3 — card size must not vary
   with band, or the run becomes uninterpretable.)
7. `wc -l` every file the worker will WRITE TO, and check what its verification command
   boots. Over ~400 lines, or a container/server boot → apply the L54 ladder above
   (excerpt-and-patch → boss extracts a small module → boss lane). Do not dispatch a lane
   whose subject you have not measured.

Cards are the boss's real deliverable. A run where four well-sized cards each delivered
beats a run where eight ambitious cards produced three corpses and one artifact.

## Worker self-defense (put this clause in every card)

```
CONTEXT: if you are about to read a file over ~200 lines, or a command is about to emit
more than ~100 lines, STOP and SendMessage 'main' asking for an excerpt or a narrower
command. Do NOT read it anyway and do NOT try to work through a compaction — a partial
worker that asked is worth more than a dead one that tried. Report what you have.
```

Workers cannot see their own context ceiling approaching in a useful way, so give them a
concrete, checkable trigger (file size, output size) instead of asking them to self-assess.

## Diagnosing a death correctly

| Symptom | Cause | Response |
|---|---|---|
| "Prompt is too long", "automatic compaction failed", context refilled to the limit repeatedly | Context, always | Re-card SMALLER at the **same band**. Never escalate the band |
| Died with a short card and quiet commands | Infrastructure flake ("API Error: Server error mid-response") — a distinct class | Re-card identically, same band. Not a capability or context finding |
| Produced nothing in a long window, no error | Often bundling (cause 3) | Check whether the card had two capabilities before assuming a stall |
| Thrash death on a card that passes the checklist — especially repeatedly, in one repo | The subject (cause 5, L54) | Measure the write target and suite. Extract a small module for the lane, or take it as a boss lane. Never re-card the same subject at any band |

**Never escalate a band for a context death.** It is the most common wrong response and it
converts a cheap failure into an expensive one.

## Salvage — a dying worker is not a lost card

Check the filesystem before re-carding (L4): a worker that died mid-task often left real
work. The best observed crash state is a written-but-unimplemented TEST FILE — the successor
inherits an executable spec instead of prose, which is an argument for the TDD-first clause
being load-bearing for crash recovery, not just for quality. Name the surviving file in the
successor's card as the specification, and mark it do-not-modify.

And record it: a dead agent that is never re-carded is a silent hole in the run. Keep the
agent roster (`boss-discipline.md` §5) and reconcile it every round — one Sentinel worker
died of context exhaustion and was never re-carded, surfacing only because the user asked.
