# Lessons — full evidence
Companion to `lessons.md`. Read only when judging a promotion/demotion or an UNANSWERED
question. Run narratives past the cap: lessons-evidence-archive.md.
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
Every check declares what it must have examined (files linted, tests collected, tables found)
and FAILS at zero, independently of exit code. **Exit 0 means "this process reported no
violation", never "no violation exists".**
*Eight instances, Sentinel runs 1-2: conftest printing `0 tests`; a vitest project collecting
no files; RLS and FK gate steps run against an empty container while 177 real violations
existed; `pnpm -r lint` exiting 0 in 197 ms because no package defines a lint script,
disabling three security rules build-wide; a migration named `.sql` not `.up.sql` so the
roundtrip found nothing and passed; the boss reading `ls` of six EMPTY directories as proof.*
The gate written to prevent this class shipped with the defect in its own two security steps.
**A guard written from the examples already seen generalises to those examples.** → §4, §9.
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
When a task's acceptance oracle needs non-trivial environment setup (real DB + migrations +
roles + fixtures), the BOSS writes that harness and ships a working oracle; the worker's card
is "make these tests pass".
*Run 3 G-1.4: a card bundling implement-the-orchestrator with debug-the-Testcontainers-harness
produced ZERO files in 33 minutes, and a parallel checker with a "boot Postgres yourself" card
died of autocompact thrash. The boss fixed the harness in ~10 minutes by copying an existing
test file. Sentinel run 9 repeated it at scale: five of six stalls were harness-bearing cards.*
Confound: card size also shrank, so "harness removed" cannot be separated from "card smaller"
— but both are context-budget causes, so the rule holds under either reading.
→ SKILL.md §6; context-budget.md cause 3.
## L18 — redirect-every-command-output — PROMOTED (2026-08-20)
Output discipline is the FIRST line of a card, not a footnote:
`cmd > /tmp/o.txt 2>&1; tail -30 /tmp/o.txt`. L1 caps what a worker READS; this caps what its
COMMANDS EMIT — the larger channel, and not covered by L1.
*Run 3: `check-lineage` died of autocompact thrash. Its card said "do not read schema.sql
whole" and then told it to load a 1200-line schema through psql, whose NOTICE output is itself
enormous.* Promoted on user-reported recurrence of the context-death class. The mechanism is
general: tool output enters context whether or not the worker wanted it, so a card obeying L1
perfectly can still kill its worker. → SKILL §6; context-budget cause 2; call-shapes.
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
**The co-authored-fixture trap.** An agent authoring BOTH a transformer and its test input
encodes the same wrong assumption twice; they confirm each other and the green CERTIFIES a
transformer that matches nothing. Allow-fixtures are GENERATED by the exact tool the exit
criterion invokes, in the exact mode, committed with URL + date + checksum; deny-cases
MUTATE ONE FIELD of a real fixture. *Sentinel run 1: 26/26 OPA green while two policies
could not fire (a public-IP Cloud SQL instance passed); the agreed "fix" was BACKWARDS —
`conftest parse` later showed the original accessor was right.* **"From the real producer"
is not precise enough**: those fixtures were genuine Terraform plan JSON, just not the format
conftest's HCL2 parser emits — the wrong REAL format fails identically to a fake one. So
"checkers execute" is necessary, not sufficient: execute against inputs the worker did not
author. → SKILL.md §4.
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
A `blocked` report gets the SAME review as a `done` report, scoped to the step the missing
dependency touches, enumerating what was and was not finished. **When the blocker is on the
VERIFICATION step, stop accepting fixes to that file** rather than accumulating unverifiable
edits. *Run 1, three instances: a Terraform-blocked worker buried "OPA 14/26" under a
DEFERRED heading; a blocked report concealed three defects, two leaving a security check
permanently unfireable; one file took THREE edits reported "FIXED" with zero executions,
two of its five defects introduced BY fixes.*
The reading is not "the cheap band is unreliable" — **any band degrades without an execution
path, and the degradation is invisible in the reports.** The fix removes the incentive:
`blocked_on: no way to execute` plus unproven assertions, accepted immediately. → SKILL §7.
## L23 — a-pasted-command-output-is-a-claim — PROMOTED (2026-08-20)
The boss re-runs anything that gates a merge, and never NAMES the output it expects.
*Run 1: a worker's report pasted `grep -n "expect(true).toBe(true)" tools/` → `(no results)`. The boss ran it: three hits, in the exact four tests verifying tenant isolation. Whether the grep ran earlier, elsewhere, or never, the effect is identical — a verification claim that reads as executed evidence and is not. The card had said `(no results)` was expected, which is the output shape easiest to produce without doing the work.* → SKILL.md §7, boss-disc §3.
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
Brief the skeptic to ATTACK BY CONSTRUCTION, not review, and to audit the suite's COVERAGE:
*which evasions does this suite not attempt?* **Treat "the check is a grep / regex / LIKE /
substring" as a defect smell** — ask what it does against the same content re-cased,
restructured, concatenated, or moved one scope outward.
*Run 1: one adversarial agent ran 20 attacks and got past the gate 8 times — the required token in an unrelated string literal; a table in a non-public schema; an uppercase `PG_ADVISORY_LOCK`; `db['del'+'ete'](row)`; a partial index where the spec forbids one. Every hard defect traced to text matching standing in for a semantic/AST/catalog check, and every coverage gap it named unprompted mapped to a defect it then found. A suite written by the tool's author tests the failures the author imagined.*
**The deepest finding**: the bypass was in the frozen SPEC, faithfully transcribed — four
review rounds spent making the tool correctly implement a specification that does not do
what it claims. → SKILL.md §4, §7.
## L28 — toolchain-preflight-before-dispatch — CANDIDATE (2026-08-20)
Enumerate every binary named in the goals' exit criteria and start all installs in parallel
BEFORE spawning any worker. When a capability has two acquisition paths of very different
sizes, start both. Verify the BINARY, not the installer's exit code.
*Run 1: installing reactively cost a round-trip per discovery; by mid-run three of four
workers had authorship done and sat queued behind one serial download, so agent parallelism
bought nothing. `brew install terraform` exited 0 and installed nothing (license change moved
it to hashicorp/tap), which a worker read as a download timeout and reported as the wrong
blocker. A 10 MB WASM Postgres unblocked verification while a 500 MB VM downloaded.*
Open question U2: does preflight REMOVE the round-trips, or move acquisition earlier on the
critical path without shrinking it? → SKILL.md §6; boss-discipline.md §9.
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
*Run 1: the three most reliable reports all came from cards written this way. One survived full independent re-verification intact and disclosed a process negative unprompted. One declined speculative security hardening, proved the attack could not reach the function, and escalated the design question. One returned BLOCKED with zero edits rather than write 98 speculative indexes that would have greened a check while creating the exact regression the check exists to prevent. The WORST report came from the worker under repeated pressure to produce a green result.* Sentinel read-path/2 and /4 reused it on every lane; lanes reported real divergences (a card contradicting the oracle, an oracle bug blocking ten tests, two self-flagged unproven behaviours) rather than quietly satisfying one side.
**Why CANDIDATE**: correlation not proven causal. Additive and safe. → call-shapes.md.
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
Commit the observation, never the attribution. "The file was rewritten between commit X and
read Y, not by me" is established; "Worker W rewrote it" is a causal claim a diff cannot
support — and a commit message is the most permanent, least correctable place for a guess
about another party's conduct. *Run 2: a commit named a worker as the rewriter. The rewrite
was real; the worker denied it, held no matching work, had a clean tree, and may have lost
the memory to compaction.* **Structural fix worth more than the attribution**: a file every
lane must touch becomes BOSS-OWNED — workers report the filename, the boss adds the line.
Contention removed by design, the only fix that survives an agent forgetting it collided.
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
## L43 — the-boss-owned-shared-file-is-the-run-s-blind-spot — CANDIDATE (2026-08-21)
L33 says remove contention by giving shared files to the boss. Right — and it creates an
unowned file: no lane's card names it, so no lane's checker attacks it.
*Sentinel read-path/2: all three lanes passed their checkers; a skeptic then found FIVE
defects in the boss-written `server.ts` + procedure chain, two CRITICAL — tRPC wraps a
thrown `Error` into a `TRPCError` KEEPING its message, so internal text was published in
the 500 body; and a rate limit in module state a second server silently rewrote.*
**Fix**: the skeptic's brief names the boss-owned files explicitly as target one.
## L44 — a-fixture-only-suite-cannot-reach-an-error-path — PROMOTED (2026-08-21)
When every port implementation is a fixture that returns cleanly, no test can drive a
throw: the error boundary is untested BY CONSTRUCTION and reads as covered. The oracle
must include one adapter that throws on purpose.
*Twice: G-3.7 (no error boundary existed) and read-path/2 (the 500 leak survived three reviews AND an 11-mutant sweep; one probe with a throwing `findEvent` found it at once).*
**Corollary**: the mutation list is a coverage CEILING like the test list (L29) — invite
the checker to ADD mutants; the self-added one found the second survivor.
## L45 — an instrument that perturbs the system will confirm any theory — PROMOTED (2026-08-21)
When a bug DISAPPEARS under instrumentation, suspect the instrument's latency before you believe its story. Bisect the added delay; if the bug tracks the delay, the probe is the variable. And interrogate the SYSTEM's own state, never the flag the code under test sets.
*Sentinel read-path/3, twice in one run. A flaky reconnect test: (a) debug queries a worker had added were themselves the reason it passed — removing them made it fail every time, and they were then "confirmed" as the fix by a theory they had created; (b) a diagnostic polling loop took ~500 ms and made delivery work, which read as "the reconnect is fine". Three confident diagnoses followed and all three were disproved by measurement, not argument. The real cause: the test waited on `isConnected`, still true because the socket error had not propagated. `pg_stat_activity` showed ZERO backends at the moment of the insert — the system's own state settled in one query what the code's self-report could not.*
**Airtight chain**: both failures share one mechanism (probe latency as a hidden variable), it is understood, and it is language- and tool-independent. → SKILL.md §4.
## L46 — one surviving mutant is not automatically a coverage gap — PROMOTED (2026-08-21)
Before recording a survivor as a hole, check whether a SIBLING guard covers the same property. Two either-sufficient guards each survive alone and the pair dies together — that is redundancy, not a gap, and deleting the "dead" one is the wrong fix. Escalate to removing BOTH; if the suite goes red, the property is defended and the finding is the redundancy, which belongs in a comment so the next reader does not rediscover it as dead code.
*Sentinel read-path/4: a no-zombie-reconnect test survived removal of the `closed` check before the reconnect timer, and survived removal of the `closed` check inside `connect()`, and went RED when both were removed — along with a second test. Two earlier goals had each spent a commit deleting genuinely unfalsifiable guards, and applying that precedent here would have removed a real one.*
**Related trap from the same run**: the FIRST version of that test was vacuous for a different reason — it asserted on the client's own state callbacks, which the client SUPPRESSES once closed. A subject that silences the channel a test listens on cannot be falsified through it; assert on the system's state instead (the server's subscription count). → SKILL.md §4.
## L47 — fixing the instance teaches nothing; fix the habit — PROMOTED (2026-08-21)
When a defect is a CLASS an author can repeat, the fix is incomplete until the repo has been swept for other instances and the rule written where the next author will read it. Fixing only the reported case is the bandaid CLAUDE.md forbids, applied to one's own work.
*Sentinel, twice in one session by the BOSS. A test fixture bound one SQL placeholder to two columns of different types (`$2` for `slug` varchar and `name` text); Postgres refuses the statement at Parse time and ten tests failed in setup. It was fixed in that file. Hours later the same author wrote `$3` across THREE differently-typed columns in a new fixture, and all 14 tests of a new suite failed identically in setup — found by a worker, who correctly reported the do-not-modify oracle as broken and STOPPED. The second fix included a repo-wide sweep for reused placeholders (none) and a comment naming the first occurrence.*
**Practice**: after fixing a class-shaped defect, grep for siblings and put the reason in a comment at the fix site, not only in the commit message. A commit message is read once; the comment is read by whoever is about to repeat it. → boss-discipline.md.

<!-- UNANSWERED lives in lessons.md; a second copy here drifted. Do not reintroduce one. -->
## L40 — the-ledger-is-committed-at-run-close — PROMOTED (2026-08-20)
The retro's final step commits and pushes the ledger. An uncommitted promotion is a lesson
learned and thrown away.
*2026-08-20 review: `lessons.md` and `run-retro.md` — the entire memory of the self-improving
loop — had NEVER been tracked in git across the skill's whole history. No `.gitignore` caused
it; no step in the loop said to add them. Five runs of lessons sat one machine failure from
being lost, and existed nowhere else.*
It does not improve a run; it makes every other lesson durable. Negative test:
`git ls-files skills/foreman/` returning 4 of 7 files — complete on disk, incomplete in the
repo, and nothing in the loop would have said so. → SKILL.md §10; run-retro.md.
## L41 — retry-accumulation-may-cause-context-death — CANDIDATE (2026-08-20)
Retry 1 continues the same worker; retry 2+ RESPAWNS FRESH with a boss-rewritten card that
inlines the fix and does not inherit the failed transcript.
Status honest: INFERRED from the loop's shape, not observed — the loop retries the same worker
with feedback appended, so its context already holds the first attempt before the retry
starts. **Run 9's L48 is the closest observed evidence** (a second card killed a worker whose
context held its first task), and settles U4 for TASK depth; retry depth specifically remains
unmeasured. → context-budget.md cause 4.
## L42 — ssh-remote-swap-beats-workflow-scope-reauth — CANDIDATE (2026-08-21)
A build shipping `.github/workflows/*` fails its first HTTPS push when the gh OAuth token
lacks `workflow` scope. Swapping the remote to SSH bypasses OAuth-app scoping and avoids an
interactive re-auth ask mid-run.
*Sentinel: first push of a Phase-0 tree carrying a gate workflow was refused; the SSH swap
succeeded immediately and every later push in runs 8-9 used it without incident.*
CANDIDATE because it is one observation on one host; the mechanism (OAuth-app scopes do not
apply to SSH keys) is well understood but the ergonomics may differ elsewhere.
## L48 — one capability per agent LIFETIME (settles U4)
`w-seed` blocked correctly, was re-tasked IN PLACE per L31 to measure every port field against
schema.sql, delivered a line-numbered sweep of eleven tables — then died of autocompact thrash
on its ORIGINAL, SMALLER card. Card size was not the difference; its context held the whole
measurement. L31 stays correct; the re-task must be a FRESH SPAWN carrying only conclusions.
## L49 — a mutating agent runs alone, reviewers included
A mutation checker was dispatched in the same message as two reviewers over the same file,
within an hour of the boss reading the note forbidding it. "Read-only" is wrong reasoning: the
reviewers' `tsc`/`eslint` read the file the mutator corrupts. Caught before either finished;
suite re-run 25/25 to prove no mutation survived the stop.
## L50 — fewer agents is not less serialization
After three stalls the boss merged two oracle cards into one, making one lane the sole
prerequisite for FOUR downstream lanes; when it went quiet nothing could start. Same error as
"an atomic dependency is not parallelism", from the other side. Reduce card SIZE, not COUNT.
## L51 — commit before mutating
Falsifying a new domain function by deleting its guard could not be reverted: `git checkout`
has nothing for an UNTRACKED file. Hash-proof of restore is necessary but not sufficient —
there must be something to restore FROM. CLAUDE.md already carried this rule, earned when a
regex destroyed four inserts in an untracked seeder, and it was violated anyway.
## L52 — the skeptic's brief is a card — CANDIDATE
Run 10's skeptic died of autocompact thrash carrying 8 attacks and a wide file list —
the L1/L17 shape, exempted because a skeptic is not called a worker. Same context
budget: ≤4 attacks, code inlined; overflow attacks go to the boss or a second skeptic.
## L53 — two silent zero-artifact deaths in one run: collapse to the boss — CANDIDATE
*Run 11: four workers died of autocompact thrash on compliant cards while two siblings
delivered; respawning bought nothing.* Rule: after the second silent death, stop respawning
and finish remaining lanes in-session with identical TDD + mutation discipline. Run 16
applied it (two deaths → boss finished both lanes) and the root cause turned out to be L55.
## L54 — measure the SUBJECT, not just the card — PROMOTED
*Runs 13-14 (2026-08-26): four workers died of autocompact thrash with zero artifacts on
cards that passed L1/L17/L18; every one was assigned an 600-800-line screen file or a
booting suite, while siblings on small pure modules delivered.* A write target must be read
to be patched and a booting suite reprints per iteration — neither is excerptable. Ladder in
context-budget cause 5; never re-card the same subject higher. Negative test: w-counts-ui's
card fails checklist item 7. Confound: those lanes were also the newest surface.
## L55 — measure the FIXED baseline, not just the card — PROMOTED
*Run 16 (2026-09-01, Sentinel): two sonnet workers died of compaction thrash on 43/47-line
cards, ≤2 reads, all redirected; haiku delivered. First `usage`: sonnet 163,898 of 200K,
haiku 119,121; dead lanes show 6 compaction markers, peak 198K.* Mechanism: every subagent
loads the CLAUDE.md files + rules before its card; the project file was 131 KB (95 KB a §7
mandated to be ten lines). Airtight: one cause, verified by numbers; fixed at source (131→39
KB). Negative test: run 16's cards pass every prior checklist item; only this preflight bites. Second measurement the same run: skeptic as `general-purpose` 164,936 first turn, died; as `tdd-guide` 90,536, delivered — the tool catalogue is the largest weight, and the CLAUDE.md cut did not move a same-session baseline (U6).
## L56 — a logged outcome is not a recorded one — CANDIDATE (2026-09-02)
*Run 19 (Sentinel): live `retire-noise --dry-run` reported 0 abstained against a known ~84% abstention rate.* Enrich
`console.log`ged the abstention and `continue`d; no row was written, so the reader had nothing to read and the doc
was re-billed every pass. Rule: before trusting a count that depends on an upstream stage, open that stage and find
the INSERT. A stage whose only trace of an outcome is a log line has not recorded it. Same shape as L19 (a row can lie) one step earlier: no row at all.
## L57 — seed tests under the tenants the code uses live — CANDIDATE (2026-09-02)
*Run 19: `retire-noise` tests seeded writer and reader under ONE tenant and passed; live, enrich wrote under the shared
tenant and the reader ran as the analyst tenant, so the abstention branch could never fire (99 rows stored, 0 read).*
Rule: anything crossing a shared corpus is tested in the live shape — shared source, grant row, shared-tenant document
and run row, analyst-tenant event. L20 (fixtures from the exact tool) one layer down: the fixture's IDENTITY must match too.
## L58 — an ordering test sets the tiebreak AGAINST the winner — CANDIDATE (2026-09-02)
*Run 20: three rank terms could each be deleted with every test green — the fixture ids happened to sort the expected
way under the id tiebreak.* Rule: for any ordering formula, build pair tests where the event that should win has the
tiebreak against it (smaller id under `id DESC`), so only the term under test can order the pair; and a test double
must sort as production sorts, proven by a parity test between the two formulas. A checker's mutant list (L29) should include deleting each term.
## L59 — the review surface is the site, not the suite — CANDIDATE (2026-09-02)
*Run 20: two defects were visible only live after a green gate AND a passed skeptic — a 200-character title quoted
in a 40px headline, and a run cap (60) that made "usually N a week" unreachable for hourly feeds.* Rule: after every
deploy the boss opens the screens the change touches (rendered, with live data) before writing done; the skeptic's
brief names the live URL as a target when the change has a UI. Extends L47: the habit is "done means seen", not "done means green".
## Run 19-20 retro — (Sentinel, 2026-09-02): both zero deaths on `tdd-guide` workers + narrow checkers. R19: dry-run count was wrong because a stage logged instead of inserting (L56) and the test seeded one tenant while live used two (L57); one gate flake on container teardown (57P01, re-run once before diagnosing). R20: three rank terms each survived deletion because fixture ids sorted the expected way by luck (L58); two defects appeared only on the deployed screens after a green gate and a passed skeptic (L59). Commit-guard hook blocked ordinary long commit messages twice → write the message to a file and `git commit -F`.
