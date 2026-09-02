# Boss discipline

The boss is the least-checked agent in the run. Everything below was earned by a
boss-side defect, not a worker's. Sentinel runs 1-2 (2026-08-19/20) produced ~30
defects; the boss authored a large share of them, including the two most expensive
single mistakes (an unverified instruction that broke a security query, and a
paraphrased exit command that hid a non-loading policy set for four review rounds).

Read this at run start alongside `lessons.md`.

## 1. Your instruction is a claim until you have run it

Execute a correction against a real substrate BEFORE sending it to a worker. Two of
five defects in one guardrail file traced to boss instructions:

- Paraphrased the goal's `conftest test infra/ --policy infra/policy` into
  `opa test infra/policy` in the card. The worker verified exactly what was asked.
  The real command could not even LOAD the policies — 26/26 green for four rounds.
- Told a worker to swap a literal `'public'` for `n.nspname`. Correct for the spec's
  query shape, illegal for the worker's (`GROUP BY` made the correlated reference
  invalid). One run against a throwaway Postgres would have caught it in 20 seconds.

**The fix that worked**: install the smallest real substrate available and run the
instruction first. `@electric-sql/pglite` (Postgres as WASM, ~10 MB, no daemon) gave a
falsifiable check in under a minute while a 500 MB Docker VM was still downloading.
Know what your stand-in can and cannot test: pglite returns `count(*)` as a JS number
where `node-postgres` returns a string, so it validates SQL correctness and is useless
for driver marshalling.

## 2. Never `git add -A` while agents are live

Three separate incidents in one run: swept a worker's in-progress files into an
unrelated commit; swept a second worker's in-flight test into a third worker's goal
commit; committed 240 MB of Terraform provider binaries, silently breaking every push
for 40 minutes. Add explicit paths, or `git add -u -- <paths>`.

Write `.gitignore` entries for tool caches (`.terraform/`, `*.tfstate*`, `node_modules/`,
`*.timestamp-*.mjs`) BEFORE running the tool that creates them.

The first incident was noted at the time as "the boss should use pathspec-scoped adds"
— and the habit continued. **A lesson recorded but not adopted is not a lesson.**

## 3. Re-run the acceptance command yourself

A worker's pasted command output is a claim, not evidence. One worker's report pasted
`$ grep -n "expect(true).toBe(true)" tools/` → `(no results)`. The boss ran it: three
hits, in the exact four tests that verify tenant isolation. Whether the greps ran
earlier, ran elsewhere, or never ran, the effect is identical — a verification claim
that reads as executed evidence and is not.

Cost of re-running: seconds. Cost of not: a silently disarmed security gate.

**And never name the output you expect.** That card said, in as many words, that
`(no results)` was the expected result. That is the output shape easiest to produce
without doing the work. Ask for the command's raw output, or run it yourself.

## 4. Clean up every resource you start, immediately

`docker ps` showed five boss verification probes still running (`mig`, `mig2`,
`schema2`, `schema-probe`, `sentinel-verify`). On a 4-CPU VM that contention was
producing a worker's `Health check failed: unhealthy` — the boss had blocked its own
worker for a full segment while telling every worker to keep the shared tree clean.

**Corollary**: an agent reporting "blocked on the environment" may be reporting a fact
about the orchestrator. Blocked reports deserve suspicion (see `lessons.md` L22) AND an
independent environment check. `docker ps` took two seconds and settled it.

## 5. Keep an agent roster and reconcile it at every round boundary

One worker died of context exhaustion and was never re-carded. The boss fixed its last
two errors by hand and lost track of the agent entirely; it surfaced only because the
user asked whether agents were still working. Idle notifications are not a roster —
a dead agent's absence is silent.

Roster row: `name | band | card | last-known state | last checked at`.

## 6. A container's existence is not evidence about its contents

`ls packages/connectors/test/fixtures` printed six source directories. The boss sent a
worker a correction asserting the fixtures existed. All six directories were empty.

Same class as `pnpm -r lint` exiting 0 in 197 ms without opening a file, and the same
class the boss had been cataloguing all day (`lessons.md` L9). `ls` of a parent, a
table's presence, a non-empty config key — none say anything about contents. Assert on
the thing you actually need.

## 7. Separate the observation from the attribution — and commit only the observation

A commit message stated that a named worker "rewrote src/schema/index.ts underneath,
dropping the events export." The rewrite was real and provable by diff. The attribution
was not: the worker denied it, held no matching work, and had a clean tree. The boss
could not distinguish a worker that wrote and lost the memory of writing (compaction)
from some other writer.

"The file was rewritten between commit X and read Y, not by me" is established and
useful. "Worker W rewrote it" is a causal claim a diff cannot support. A commit message
is the most permanent and least correctable place to put a guess about someone's conduct.

**Structural fix worth more than the attribution**: the shared barrel file is now
boss-owned exclusively — workers add modules and report the filename, the boss adds the
export line. Contention removed by design, not by coordination discipline, which is the
only kind of fix that survives an agent forgetting it collided.

## 8. Do not accuse of fabrication before checking

Off the back of the bad `ls` above, a worker described real fixture bytes it held. It
read exactly like a worker inventing file contents to satisfy a boss who had just
insisted they existed. The boss was one message from accusing it. The bytes were real,
recorded by curl from the real endpoints, sitting in `/tmp` rather than the repo — byte
counts matched the report exactly.

**An unverified accusation of fabrication is itself a fabrication.** Check especially
when the claim is inconvenient, or looks too convenient.

## 9. Toolchain preflight before dispatch

Enumerate every binary named in the goals' exit criteria (`terraform`, `conftest`,
`opa`, `docker`, `psql`, `k6`, `gh`, validators) and start all installs in parallel
BEFORE spawning any worker. Installing reactively cost a round-trip per discovery, and
by mid-run three of four workers had authorship done and were queued behind a single
serial download. Agent parallelism bought nothing during that window.

**When a blocked capability has two acquisition paths of very different sizes, start
both.** The 10 MB WASM Postgres unblocked verification while the 500 MB VM downloaded.

Verify the binary exists, do not trust the installer's exit code: `brew install terraform`
exits 0 and installs nothing (license change moved it to `hashicorp/tap`). A worker read
that as a download timeout and reported the wrong blocker.

## 10. A plausible ambient explanation is the most dangerous kind

A push failed for 40 minutes and was diagnosed as "slow network" — which was
independently true all afternoon. The real error (`GH001: Large files detected`) had
been sitting in the background task's output file the whole time.

The boss spent the run telling workers to assert from output rather than expectation,
and then accepted a theory it already believed instead of reading the failure text.

## 11. Verify through the path production uses

A tenant-isolation fix landed in `policies/*.sql` (4 of 4 files) and NOT in the
migration that every real environment is built from — 124 unfixed occurrences. Every
boss check said green, because the boss had been hand-applying the schema it fixed.

Same shape, second instance: a decision to install PostGIS into a dedicated schema was
recorded in an ADR, agreed, and never implemented — and the gate could not see it,
because the gate builds its database from different inputs than production does.

**A decision is not applied until a command shows it applied.** "Recorded in the run
log" and "agreed in an ADR" are both upstream of the diff. And when a check and the
environment it protects are built from different inputs, the check is not testing the
environment.

## 12. Record what you did, never what you concluded exists

A worker could not find WHO's Disease Outbreak News endpoint, correctly refused to
invent one, and then wrote in a source comment that no public endpoint exists. It does.
That comment removed the product's highest-tier source, and read as settled fact to
everyone downstream, for as long as it survived.

"Searched X, Y, Z on <date>, found no public endpoint" is honest and re-checkable.
"There is no public endpoint" is a claim about the world that one failed search cannot
support — and in a comment it outlives the search that produced it.

Same rule for fixtures: record URL + date + checksum next to every recorded payload. A
fixture whose origin is unrecorded is indistinguishable from a fabricated one within
months.

## 13. Scope safety exceptions to named paths, never to a glob class

Every pattern-ban rule (lint rule, secret scanner, anti-goal grep) flags its own
definition and its own tests. This is structural. The obvious exception —
`files: ["**/*.test.ts"]` — would have disabled three security rules across every test
file in the repo forever, and tests are exactly where a raw DB handle gets written
casually.

If you can state the exception as "tests are exempt", it is too broad. The correct form
is "these three files, because X", with a note not to widen it.

## 14. Kernel work is built serially by the boss

Load-bearing primitives (the tenant-context wrapper, the auth boundary, the money path)
are not fanned out. They are small, they are the thing every other lane depends on, and
a retry loop on them costs more than writing them.

## 15. Re-task a blocked agent to measure the blocking question

Twice, an agent blocked on an unresolvable guardrail conflict was re-tasked to produce
the measurement that settles it, rather than idled. The larger of the two produced a
384-line ADR with real `EXPLAIN (ANALYZE, BUFFERS)` plans over 470k synthetic rows, and
one line of `\di+` output killed the compromise everyone's intuition reaches for
(index sizes 3160 kB vs 3272 kB — a "cheap extra index" is a second full index).

Waiting for a human to arbitrate between two arguments produces a worse decision more
slowly. Turn the argument into a decision.

## 16. Your card's test list is the coverage ceiling

A card enumerated six self-test cases. The case it omitted ("table with RLS enabled but
NO policy at all") was exactly where the tool had a permanently dead branch. **A worker
will not invent the case you omitted.** Boss-authored test enumerations are a
load-bearing artifact — review them for completeness before dispatch, not after.

## 17. Fixing the instance teaches nothing — fix the habit (L47)

A defect that is a CLASS, not a one-off, is not fixed until the repo has been swept for
siblings and the reason written where the next author will read it.

Twice in one session the boss bound a single SQL placeholder to columns of different
types (`$2` for a varchar and a text column; later `$3` across three). Postgres refuses
the statement at Parse time, so every test in the suite fails in setup, pointing at the
fixture rather than at anything under test. The first was fixed in place and taught
nothing; the second cost a worker a full segment and was found only because it reported
the do-not-modify oracle as broken and stopped instead of guessing.

**The fix has three parts**: correct the instance, `grep` for siblings across the repo,
and leave a comment AT the fix site naming the class. A commit message is read once by
whoever merges it; the comment is read by whoever is about to repeat the mistake.
