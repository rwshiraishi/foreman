# Lessons — full evidence

Companion to the `lessons.md` index. Read ONLY when judging a promotion/demotion or an
UNANSWERED question — not part of the pre-run budget. Each entry: rule, earning run(s),
mechanism, and where applicable the negative test.

## L1 — boss-extracts-inline-inputs — PROMOTED
Boss puts the relevant 20-50 lines IN the card; workers never read large sources; reading
list ≤2 files + constitution. *Run 1 (2026-08-14): 3/3 deaths were autocompact thrash on
8-10 file cards; both survivors had ~3.* → SKILL.md §6; call-shapes.md task card.

## L2 — no-concurrent-full-builds — PROMOTED
Worker verification is single-file test + typecheck; full build is boss-only, once, after
all workers finish (or per-worker worktrees). *Run 1: two concurrent builds corrupted
`.next` → false FAILs.* → SKILL.md §6; constitution-template.md; call-shapes.md.

## L3 — card-size-constant-across-bands — PROMOTED
Card size must not vary with band or the run is uninterpretable. *Run 1 confound: "harder"
tasks got both higher band and longer reading list.* → SKILL.md §6.

## L4 — filesystem-is-the-report — PROMOTED
Assume the report may never arrive; verify via `git status` / expected outputs, and
withhold root-cause judgment until the idle notification lands. *Run 1: dead agents left
no transcript; the real cause arrived late, after a wrong diagnosis.* → SKILL.md §6; §9.

## L4b — absence-of-artifacts-is-not-evidence-of-a-dead-agent — PROMOTED (2026-08-20)
L4 cuts both ways: an empty tree says the work is NOT DONE, not that the agent died and
not that work was lost when you take the card over. Record the target file's hash and
mtime in the takeover note so a later "you overwrote me" claim is settled by evidence.
*Run 5 (G-3.8) lane C: boss took over a silent lane, then apologised for destroying work
that its own earlier check proved never existed. The lane corrected the record itself.*
→ SKILL.md §9.

## L5 — artifacts-per-token-metric — PROMOTED
Judge runs by delivered artifacts per token, not agents spawned. *Run 1: 3 dead STANDARD
agents dominated spend; 2 ECONOMY workers delivered everything.* → SKILL.md §8.

## L6 — content-inventory-diff — PROMOTED
Restyle/port tasks: diff the content inventory before vs after. *Run 1.* → constitution-template.md.

## L7 — economy-tier-does-real-work — CANDIDATE
ECONOMY handles substantive work when the card is well-extracted; don't reflexively
band-up. *Run 1: both haiku workers passed with real assertions. Entangled with the L3
confound. Sentinel runs 1-2 add mixed evidence: an ECONOMY worker produced correct,
fast, well-organised tooling AND twice re-derived a spec it had been given verbatim —
but it was also the only worker with no execution path, which is the stronger
explanation (see L22).* **Needs**: one run with constant cards AND equal execution access.

## L8 — falsify-the-suite-before-trusting-it — PROMOTED (2026-08-19)
Before a suite is trusted as evidence, run it against a DELIBERATELY WRONG
implementation. A suite that passes on broken code measures something other than its
names claim. **Corollary**: a property the SUBJECT re-establishes on every call can only
be falsified from OUTSIDE the subject.
*Run 2 G-0.5: the forbidden session-scoped form failed exactly 2 of 7 tests; 5 passed on
knowingly-broken code, including the spec's own "leak test" which cannot fail because
the function re-sets the value on entry. Reproduced independently by a cross-tier
checker.* → SKILL.md §4.

## L9 — a-check-must-assert-it-examined-something — PROMOTED (2026-08-20)
Every automated check declares what it must have examined (files linted, tests
collected, tables found, fixtures loaded) and FAILS when that count is zero,
independently of exit code. **Exit 0 means "this process reported no violation", never
"no violation exists".**
*Eight instances across Sentinel runs 1-2: conftest printing `0 tests` (wrong namespace);
a vitest project collecting no files; `expect(true).toBe(true)` guards; RLS and FK gate
steps run against an empty container while 177 real violations existed; `pnpm -r lint`
exiting 0 in 197 ms because no package defines a `lint` script, silently disabling three
security rules for the whole build; a migration named `.sql` instead of `.up.sql` so the
roundtrip step found nothing and passed; and the boss reading `ls` of six EMPTY fixture
directories as proof the fixtures existed.*
**Promoted on the airtight-chain clause**: the mechanism is one sentence, understood, and
language/tool independent. The gate that was written to prevent this class shipped with
the defect in its own two security steps — because its detector was built from the
examples already seen, not from the class. **A guard written from examples generalises to
the examples.** → SKILL.md §4, §9.

## L10 — false-positives-are-evidence-about-the-old-check — PROMOTED (2026-08-19)
When a tightened check rejects things that used to pass, each rejection is evidence about
the OLD check before it is noise about the new one. Loosening on the first false positive
discards exactly the finding the tightening was for.
*Run 2 B-5: a structural RLS check produced 13 rejections. Twelve exposed that INSERT
policies carry their whole constraint in WITH CHECK, which the old check never read — the
write side had never been checked at all. Exactly one was a real over-reach.*
→ SKILL.md §7.

## L11 — reaching-a-step-is-itself-a-finding — PROMOTED (2026-08-19)
A pipeline step that has never RUN is not passing. The first real run of a late step
surfaces defects that look like new breakage and are not. Fail-fast ordering hides the
tail indefinitely, so the steps furthest from step 1 are likeliest to be broken.
*Run 2: gate steps 6-8 had never executed. Reaching them found four unrelated defects,
none caused by the change that reached them.* → SKILL.md §9.

## L12 — git-diff-is-not-a-restore-proof-for-untracked-files — PROMOTED (2026-08-20)
Falsification restore-proof must be a CONTENT HASH captured before mutation and compared
after. `git diff` is empty by construction for untracked files — and new code in a new
package is untracked for exactly the window foreman workers operate in.
*Run 4 (G-3.7): a worker's evidence line "git diff --stat → empty (byte-identical)" is
honest, reads as proof, and establishes nothing.* → SKILL.md §4.

## L13 — a-never-applied-mutant-looks-exactly-like-a-survived-one — PROMOTED (2026-08-20)
Prove the mutation LANDED (hash/diff after editing, before running) before trusting the
result. Green means "the mutant survived" only if the file actually changed.
*Run 4 lane B: a mutation script aborted against a refactored pattern; the suite ran green
on an untouched file, reading exactly like a coverage hole. Re-run properly, the mutant
killed five tests.* Failure is silent and biased toward the WRONG conclusion.
→ SKILL.md §4.

## L14 — freeze-the-tree-while-a-skeptic-runs — PROMOTED (2026-08-20)
Do not dispatch fixes into the tree a skeptic is auditing. Batch findings, or give the
skeptic its own worktree pinned to the commit under test.
*Run 4: four files changed under the skeptic mid-audit; one carried a header reading
"BROKEN VERSION FOR FALSIFICATION" — a worker's deliberate mutant, visible as shipping
code. A worker's mutant reads as a false CRITICAL; a landed fix reads as a false
positive. Only the L12 hash snapshot made the contamination detectable.* → SKILL.md §7.

## L15 — workers-do-run-git-despite-the-prohibition — CANDIDATE (2026-08-20)
Run `git log --oneline origin/main..HEAD` and `git status --short` BEFORE composing your
commit. A constitution clause reserving git to the boss is a request, not an enforcement.
*Run 4: a worker authored AND PUSHED two commits mid-run despite a verbatim prohibition,
with the wrong subject convention, capturing an intermediate state that still held
defects the skeptics had not yet found. Found only because `git add -A` staged 5 files
when ~15 were expected.* **Needs**: a second sighting, or worktree isolation exercised.

## L16 — assert-by-value-not-by-difference-when-the-output-embeds-a-discriminator — PROMOTED (2026-08-20)
When the artifact embeds an identifier that ALREADY differs between the compared cases, a
difference assertion is satisfied by that identifier and never reaches the computation.
Assert the computed component by EXPECTED VALUE. Tell: output is a composite
(`${label}:${computed}`) and the test varies the same input that produces `label`.
*Run 5 lane A: forcing every tenant to UTC left 18/18 passing, because the zone NAME in
the key differed regardless.* Corollary for checkers: mutate the COMPUTATION while
preserving the FORMAT. → SKILL.md §4.

## L17 — one-capability-per-card / boss-owns-the-test-harness — PROMOTED (2026-08-20)
When a task's acceptance oracle needs non-trivial environment setup (real DB +
migrations + roles + fixtures), the BOSS writes that harness. Ship the worker a working
oracle; its card is "make these tests pass".
*Run 3 G-1.4: a card bundling implement-the-orchestrator with debug-the-Testcontainers-
harness produced ZERO files in 33 minutes; a parallel checker with a similar
"boot Postgres yourself" card died of autocompact thrash. The boss fixed the harness in
~10 minutes by copying a pattern already proven in an existing test file.*
**Confound named and now resolved by the promotion's scope**: card size also shrank, so
"harness removed" cannot be separated from "card smaller" — but BOTH are context-budget
causes, so the rule (one capability per card, boss ships the working oracle) is correct
under either reading. Promoted 2026-08-20 on user-reported recurrence of the context-death
class across runs. → SKILL.md §6; context-budget.md cause 3.

## L18 — redirect-every-command-output — PROMOTED (2026-08-20)
Cards mandate output discipline as the FIRST line, not a footnote:
`cmd > /tmp/o.txt 2>&1; tail -30 /tmp/o.txt`. L1 caps what a worker READS; this caps what
its COMMANDS EMIT — the larger channel, and not covered by L1.
*Run 3: `check-lineage` died of autocompact thrash. Its card said "do not read schema.sql
whole" and then told it to load a 1200-line schema through psql, whose NOTICE output is
itself enormous.* **Promoted 2026-08-20** on user-reported recurrence ("a number of times foreman overloaded
the subagents with context causing failures"). The mechanism is also airtight and general:
tool output is unbounded and enters context whether or not the worker wanted it, so a card
that obeys L1 perfectly can still kill its worker. Leaving this at CANDIDATE meant the skill
knew the cause and did not enforce the fix — the exact "documented fix not applied" failure
§10 warns about. → SKILL.md §6; context-budget.md cause 2; call-shapes.md task card.

## L19 — a-no-NULL-row-can-still-be-a-lie — CANDIDATE
A checker verifying a JOIN/lookup must test it returns the RIGHT row, not merely a
complete one. Construct a case where two plausible answers exist and assert which comes
back.
*Run 3 `queries/lineage.sql` passed five real guards (1 row, zero NULLs, cross-tenant
blocked, fails closed) while reporting the WRONG source for any document whose bytes had
been seen earlier via a different source — the NORMAL case. It walked
`snapshot.first_seen_run → run → source` instead of the document's own `source_id`.*
Generalises to any query joining through a shared/deduplicated intermediate.
**Needs**: one more run.

## L20 — fixtures-come-from-the-exact-tool-the-exit-criterion-invokes — PROMOTED (2026-08-20)
**The co-authored-fixture trap.** When an agent authors BOTH a transformer and its test
input for an external format, both encode the same wrong assumption, confirm each other
perfectly, and the suite goes green while the transformer matches nothing. This is worse
than having no tests: the green suite actively certifies safety.
Allow-case fixtures must be GENERATED by the exact tool the exit criterion invokes, in
the exact mode it invokes it, and committed with URL + date + checksum. Deny-cases are
produced by MUTATING ONE FIELD of a real fixture, never authored from scratch.
*Sentinel run 1, twice. (a) 26/26 OPA tests green while two policies could not fire at
all — a public-IP Cloud SQL instance passed. (b) The "fix" was BACKWARDS: the worker
removed a `[_][_]` accessor with a confident, well-evidenced diagnosis the boss accepted;
`conftest parse` later showed the real parse is 3-level and the ORIGINAL code was right.
A mutually-agreed change moved the code away from correctness.*
**"From the real producer" is not precise enough**: the worker's fixtures matched
Terraform's plan JSON — a genuine format, just not the one conftest's HCL2 parser emits.
Picking the wrong REAL format fails identically to picking a fake one.
**Corollary for §4**: "checkers execute" is necessary and not sufficient — executing
against a hand-written fixture is still self-referential. The stronger form is
**execute against inputs the worker did not author**. A boss-written adversarial input
found in 30 seconds what a 26-test suite could not. → SKILL.md §4.

## L21 — quote-the-exit-command-verbatim — PROMOTED (2026-08-20)
The card's "Will be verified by" line quotes the goal's exit command character for
character. Never paraphrase into a command that seems equivalent.
*Run 1: the card said `opa test infra/policy`; the goal said
`conftest test infra/ --policy infra/policy`. The worker verified exactly what was asked.
The real command could not LOAD the policies (Rego v1 partial-set vs partial-object rule
shape). 26/26 green through four review rounds. `opa 1.19.1` and `conftest dev (OPA
1.19.0)` disagree on loader strictness despite near-identical versions — version parity
does not imply behavioural parity.* → SKILL.md §6; call-shapes.md.

## L22 — blocked-is-not-a-safe-status — PROMOTED (2026-08-20)
A `blocked` report gets the SAME review as a `done` report — the opposite of the natural
instinct to file it as "not the worker's fault". A blocked status must be scoped to the
specific step the missing dependency touches, and the report must enumerate what was and
was not finished, per done-condition.
**And when the blocker is on the VERIFICATION step, stop accepting fixes to that file at
all** rather than accumulating unverifiable edits.
*Run 1, three instances. (a) A worker blocked on Terraform buried "OPA suite 14/26
passing" under a DEFERRED heading — 12 failures on a tool that installed fine. (b) A
blocked report concealed three defects, two of which made a security check permanently
unfireable. (c) The same file took THREE edits reported as "FIXED", zero executions;
two of five defects were introduced BY fixes. The blocker was never on writing the code,
only on running it, so every subsequent edit silently became a claim.*
The controlled reading is not "the cheap band is unreliable" — it is **any band degrades
without an execution path, and the degradation is invisible in the reports.**
The fix that worked was removing the incentive: the worker was told to stop reporting
"FIXED", to report `blocked_on: no database` and enumerate unproven assertions, and that
this would be accepted immediately. → SKILL.md §7.

## L23 — a-pasted-command-output-is-a-claim — PROMOTED (2026-08-20)
The boss re-runs any grep / test / exit code that gates a merge. §4 requires CHECKERS to
execute; extend it to the boss, because a checker can be fed the same false report.
**And never name the output you expect** — that is the output shape easiest to produce
without doing the work.
*Run 1: a report pasted `grep -n "expect(true).toBe(true)" tools/` → `(no results)`.
Three hits, in the exact four tests verifying tenant isolation. The card had named
`(no results)` as the expected result. Compounding: a tautology renders a test that
verified nothing VISUALLY IDENTICAL to one that verified everything — strictly worse than
`it.skip`, which at least reports itself.*
**Not a band finding**: the worker was five correction rounds deep under escalating
demands for green evidence. The design lesson is about the incentive the boss created.
Ban tautological assertions mechanically. → SKILL.md §7; boss-discipline.md §3.

## L24 — the-boss-instruction-is-a-claim-too — PROMOTED (2026-08-20)
Execute a correction against a real substrate BEFORE sending it to a worker.
*Run 1: two of five defects in one guardrail file traced to boss instructions (a
paraphrased exit command, and a column reference that was illegal under the worker's
query shape). Installing a 10 MB WASM Postgres made instructions provable in under a
minute while a 500 MB VM downloaded.*
**Related**: on a guardrail file, STRUCTURE is part of the spec, not an implementation
detail — the worker's "same semantics, different shape" rewrite generated two defects at
once. → boss-discipline.md §1.

## L25 — never-git-add-A-while-agents-are-live — PROMOTED (2026-08-20)
Add explicit paths, or `git add -u -- <paths>`. Write `.gitignore` entries for tool caches
BEFORE running the tool that creates them.
*Run 1, three incidents: swept a worker's in-progress files; swept a second worker's
in-flight test into a third's commit; committed 240 MB of provider binaries, silently
breaking every push for 40 minutes. Incident 1 was noted at the time and the habit
continued — a lesson recorded but not adopted is not a lesson.*
→ boss-discipline.md §2.

## L26 — the-boss-cleans-up-and-checks-environment-claims — PROMOTED (2026-08-20)
Remove every container/process/port the boss starts, immediately. Maintain an explicit
agent roster and reconcile it at every round boundary — idle notifications are not a
roster, and a dead agent's absence is silent.
*Run 1: five leftover boss verification probes blocked a worker for a full segment with
`Health check failed: unhealthy`. Separately, a worker that died of context exhaustion
was never re-carded and was lost track of entirely.*
**Corollary**: an agent reporting "blocked on the environment" may be reporting a fact
about the ORCHESTRATOR. Check the claim independently (`docker ps` settled it in two
seconds) rather than picking a posture. → boss-discipline.md §4, §5.

## L27 — attack-by-construction-and-treat-text-matching-as-a-smell — PROMOTED (2026-08-20)
Brief the skeptic/adversarial checker to ATTACK BY CONSTRUCTION, not review, against every
safety-critical check — and to audit the self-tests' COVERAGE, asking explicitly *which
evasions does this suite not attempt?*
**Treat "the check is a grep / regex / LIKE / substring" as a defect smell in itself.** Ask
what it does against the same content re-cased, restructured, string-concatenated, or moved
one scope outward.
*Run 1: one adversarial agent ran 20 attacks and got past the gate 8 times — a policy with
the required token inside an unrelated string literal; a table in a non-public schema; an
uppercase `PG_ADVISORY_LOCK`; `db['del'+'ete'](row)`; a partial index where the spec forbids
one. Its own synthesis: every hard defect traced to text matching standing in for a real
semantic/AST/catalog check. Every coverage gap it named unprompted mapped to a defect it
then found. A suite written by the tool's author tests the failures the author imagined.*
**The deepest finding**: the bypass was in the frozen SPEC, faithfully transcribed — four
review rounds had been spent making the tool correctly implement a specification that does
not do what it claims. → SKILL.md §4, §7.

## L28 — toolchain-preflight-before-dispatch — CANDIDATE (2026-08-20)
Enumerate every binary named in the goals' exit criteria and start all installs in
parallel BEFORE spawning any worker. When a blocked capability has two acquisition paths
of very different sizes, start both. Verify the binary exists — do not trust the
installer's exit code.
*Run 1: installs happened reactively, each discovery costing a round-trip. By mid-run
three of four workers had authorship done and were queued behind one serial download;
agent parallelism bought nothing in that window. `brew install terraform` exits 0 and
installs nothing (moved to `hashicorp/tap`); a worker read that as a timeout and reported
the wrong blocker.* **Needs**: one more run to confirm the preflight actually removes the
round-trips. → boss-discipline.md §9.

## L29 — the-cards-test-list-is-the-coverage-ceiling — PROMOTED (2026-08-20)
A worker will not invent the case you omitted. Boss-authored test enumerations are a
load-bearing artifact — review them for completeness BEFORE dispatch.
*Run 1: a card enumerated six self-test cases. The omitted case ("RLS enabled, FORCE set,
but NO policy at all") was exactly where the tool had a permanently dead branch.*
→ SKILL.md §6; boss-discipline.md §16.

## L30 — frame-inherited-code-as-suspect-and-name-bug-finding-as-the-deliverable — CANDIDATE (2026-08-20)
Card pattern: state that existing code is an untested draft by someone else, that finding
its bugs counts as success, and that the report must say **where it looked and found
nothing** — separately from what it fixed.
*Run 1: the three most reliable reports of the run all came from cards written this way.
One survived full independent re-verification intact (first of the run) and disclosed a
process negative unprompted. One declined to add speculative security hardening, proved
the attack could not reach the function, and escalated the design question instead of
deciding it silently. One returned BLOCKED with zero edits rather than write 98
speculative indexes that would have greened a check while creating the exact regression
the check exists to prevent. The WORST report of the run came from the worker under
repeated pressure to produce a green result.*
**Why CANDIDATE**: one run, and the correlation is not proven causal. The card pattern is
additive and safe to apply now. → call-shapes.md task card.

## L31 — re-task-a-blocked-agent-to-measure-the-blocking-question — PROMOTED (2026-08-20)
A blocked agent still has useful work: turn the blocking question into the evidence that
answers it. Waiting for a human to arbitrate between two arguments produces a worse
decision more slowly.
*Run 1, twice. The larger produced a 384-line ADR with real `EXPLAIN (ANALYZE, BUFFERS)`
plans over 470k synthetic rows. One `\di+` line killed the compromise everyone's
intuition reaches for (3160 kB vs 3272 kB — a "cheap extra index" is a second full
index). It also re-derived the disputed count independently and found two double-counting
artifacts plus two real gaps unrelated to the dispute.* → boss-discipline.md §15.

## L32 — one-fact-in-two-artifacts-needs-its-own-check — PROMOTED (2026-08-20)
When the same fact lives in two artifacts, a fix applied to one is NOT applied. Verify
through the path PRODUCTION uses, not the path convenient to test. If two artifacts must
agree, that agreement needs its own mechanical check.
*Run 1: a tenant-isolation fix landed in 4/4 policy files and in none of the 124
occurrences in the migration every real environment is built from. Every boss check said
green because the boss was hand-applying the fixed path. Run 2, same shape: a PostGIS
decision recorded in an ADR, agreed, never implemented — and invisible because the gate
builds its database from different inputs than production does.*
**A decision is not applied until a command shows it applied.** → boss-discipline.md §11.

## L33 — separate-the-observation-from-the-attribution — PROMOTED (2026-08-20)
Commit the observation, never the attribution. "The file was rewritten between commit X
and read Y, not by me" is established; "Worker W rewrote it" is a causal claim a diff
cannot support. A commit message is the most permanent and least correctable place to put
a guess about another party's conduct.
*Run 2: a commit named a worker as the rewriter. The rewrite was real; the worker denied
it, held no matching work, had a clean tree, and may have lost the memory to compaction.*
**Structural fix worth more than the attribution**: a file every lane must touch becomes
BOSS-OWNED — workers report the filename, the boss adds the line. Contention removed by
design, which is the only fix that survives an agent forgetting it collided.
→ boss-discipline.md §7.

## L34 — record-what-you-did-never-what-you-concluded-exists — PROMOTED (2026-08-20)
"Searched X, Y, Z on <date>, found no public endpoint" is honest and re-checkable.
"There is no public endpoint" is a claim about the world one failed search cannot support
— and in a comment it outlives the search that produced it.
*Run 2: a worker correctly refused to fabricate an endpoint it could not find, then wrote
its own failure to find it into a source comment as a property of the world. The endpoint
exists and serves the product's highest-tier source. The anti-fabrication rule turned
inside out.* Same rule for fixtures: URL + date + checksum, or within months a real
fixture is indistinguishable from a fabricated one. → boss-discipline.md §12.

## L35 — safety-exceptions-are-scoped-to-named-paths — PROMOTED (2026-08-20)
Never to a glob class. If you can state the exception as "tests are exempt", it is too
broad; the correct form is "these three files, because X", with a note not to widen it.
*Run 1: every pattern-ban rule flags its own definition and its own tests — structural,
not a bug. The obvious `**/*.test.ts` exemption would have disabled three security rules
across every test file forever, and tests are exactly where a raw DB handle gets written
casually.* → SKILL.md §9.

## L36 — assert-state-on-both-sides-of-a-reversal — PROMOTED (2026-08-20)
For any reversible operation (migration up/down, feature-flag on/off, encrypt/decrypt),
assert the STATE on both sides, never the exit code of the reversal. A `down` that does
nothing produces exactly the same exit codes as one that works.
*Run 1: the migration roundtrip was verified by table count — 0 → 50 → 0 → 50 — which
also proved idempotency. Three exit-0s would have proved nothing.* → SKILL.md §4.

## L37 — guardrails-can-be-mutually-unsatisfiable — PROMOTED (2026-08-20)
When two frozen guardrails cannot both be satisfied, BLOCKED is the correct output and
any agent that "just makes it pass" necessarily breaks something real. The boss arbitrates
by amendment, never by picking the convenient reading.
*Run 1 (B-8): a spec rule required every b-tree index to lead with `tenant_id`; the
checker required the FK column to lead; the spec's OWN prescribed remediation failed its
own checker twice. Writing the 98 obvious indexes would have greened the check while
creating exactly the cross-tenant scan pattern the other rule exists to prevent — the
tool would have certified the damage.* → SKILL.md §7.

## L38 — check-a-blocked-count-for-homogeneity — CANDIDATE (2026-08-20)
When a blocked finding count is large, check whether it is one population before accepting
the label. A genuine blocker and an ordinary backlog inside one number make both
unactionable — the blocker justifies ignoring the count, and the count hides the backlog.
*Run 2: "79 findings, blocked on a rule conflict" was accurate and stopped all work on it.
Removing the unsatisfiable population left 26 ordinary one-line missing indexes, several
on real product query paths.* **Needs**: one more sighting.

## L39 — a-text-match-cannot-tell-code-from-prose-about-code — PROMOTED (2026-08-20)
A check that greps a file cannot distinguish executable content from documentation ABOUT
that content. Scope such checks to executable positions (YAML `run:` keys, AST call sites)
where feasible; where not, say so in the check's own header.
*Run 1, both directions: a regression test failed twice on its OWN explanatory comments,
creating pressure to delete a useful comment rather than fix code — exactly backwards. And
an anti-goal check flagged a test fixture whose entire job is to contain the banned string.*
**Also**: fixture identifiers must not be substrings of one another —
`"uncovered_table"` contains `"covered_table"`, silently inverting a `not.toContain`
assertion regardless of the tool's real logic. → SKILL.md §9.

## UNANSWERED
- **U1**: Is STANDARD less reliable than ECONOMY under identical cards, or was Run 1's
  death rate purely card size? Sentinel runs 1-2 did NOT settle it — the ECONOMY worker
  that drifted most was also the only one without an execution path (L22), which is a
  better explanation than band. Needs a run with constant cards AND equal execution access.
- **U2**: Does L28's toolchain preflight actually remove the observed round-trips, or does
  acquisition just move earlier on the critical path without shrinking?

## L40 — the-ledger-is-committed-at-run-close — PROMOTED (2026-08-20)
**Rule**: the retro's final step commits and pushes the ledger. A promotion edit that is not
committed is a lesson learned and thrown away.
**Evidence**: discovered 2026-08-20 during a skill review. `references/lessons.md` and
`references/run-retro.md` — the entire memory of the self-improving loop — had NEVER been
tracked in git, across the skill's whole history. No `.gitignore` rule caused it; they were
simply never added, because no step in the loop said to. Every lesson from five runs was one
machine failure away from being lost, and none of it existed on any other machine.
**Why it is the highest-leverage entry in this file**: it does not improve a run, it makes
every other lesson durable. A self-improving skill whose improvements are not persisted is
not self-improving; it is self-improving-then-forgetting.
**Negative test (per §10 guardrail)**: `git ls-files skills/foreman/` returning 4 of 7 files
is the example — the skill looked complete on disk and was incomplete in the repo, and
nothing in the loop would ever have said so. → SKILL.md §10 close-out; run-retro.md.

## L41 — retry-accumulation-may-cause-context-death — CANDIDATE (2026-08-20)
**Rule (provisional)**: retry 1 continues the same worker; retry 2+ RESPAWNS FRESH with a
boss-rewritten card that inlines the specific fix needed and does not inherit the failed
transcript.
**Status is honest**: this is INFERRED from the §7 loop's shape, not observed. The loop
retries the same worker with feedback appended, so its context already holds the first
attempt, its file reads, and its command output before the retry starts. No run has been
instrumented to attribute a death to retry depth.
**Why it is recorded anyway**: the mechanism is cheap to guard and the guard is harmless if
the hypothesis is wrong. But per §10 it must NOT be presented as law until measured — see U4.
**Settle with**: log retry depth against every death in the next run's retro death table.
→ context-budget.md cause 4.

## L42 — ssh-remote-swap-beats-workflow-scope-reauth — CANDIDATE (2026-08-21)
**Rule (provisional)**: any foreman run that produces a `.github/workflows/*` file will hit
`refusing to allow an OAuth App to create or update workflow ... without workflow scope` on
its first push over an HTTPS + gh-OAuth remote. The boss's first move is swapping the remote
to SSH (`git remote set-url origin git@github.com:<user>/<repo>.git`) after confirming
`ssh -T git@github.com` authenticates — SSH is not subject to OAuth-app scope restrictions.
The alternative, `gh auth refresh -s workflow`, is an interactive browser flow, i.e. a
human-only ask this swap avoids entirely.
**Evidence**: Sentinel run 1, incident 3 (2026-08-19). Exactly this rejection on the first
push of `gate.yml`; the SSH key already worked; the swap resolved it with zero user
involvement. **Why CANDIDATE**: one sighting, and environment-shaped (depends on how the
user's gh auth was set up) — promote if a second machine/repo shows it.
