# Lessons evidence — archived run narratives

Moved out of the read path at the 450-line cap (SKILL §10). Lesson entries stay in
lessons-evidence.md; only run narratives land here.

## Run 10 — 2026-08-24 — Sentinel enrich/live-llm (LLM reads WHO corpus; map + disease filter live)
**Job**: VertexProvider, reference load, svc-enrich, projection, API concept filter, map UI.
**Setup**: 56-line constitution; 9 STANDARD cards; 2 scouts. **Targeting**: none apply.
Deaths (cause class context unless noted): w-enrich (bundled harness+flow, 6-case card),
w-api (697-line test file in reading list), w-ui (fixture sweep across 5 files), skeptic
(8 attacks + wide file list); w-loadref infra-flake (server error mid-response), recarded fresh
→ passed. Survivors: w-refcsv, w-vertex, w-enrich2 (respawn, oracle-only card, 2 correct
BLOCKs on real scaffold gaps), w-loadref2, w-project — all passed checks the boss re-ran.
**Worked**: boss-shipped oracle + "make these tests pass" respawn (w-enrich2); salvage of
w-ui at ~90% (compiler enumerated the remainder); collapse-to-boss for the API lane after 2
deaths; measured-not-guessed everywhere (owner probe, timing logs, Context7 pg_trgm).
**Failed**: 4/10 agents died of context — all boss card-authoring faults matching L1/L17
shapes already in the ledger. **Confounds**: none blocking.
**Artifacts/token**: STANDARD carried everything delivered; deaths dominated waste.
**Fixes applied mid-run**: L4 salvage yes; L17 boss-harness yes; infra-flake recard yes.

## Run 11 — 2026-08-25 — Sentinel map-and-score + satellite lane (Run 10 in archive)
**Delivered**: satellite basemap (deployed), svc-score live (50/50), ADR 0019 live,
Scheduler chain, events-concepts test. **Deaths**: 4 workers + skeptic, autocompact
(L53/U5); w-geojson a SIXTH, different class — mid-response API error, certificate
10h late (L4 held: work was already rebuilt by the boss from git-status evidence).
**Survived**: w-sched (ECONOMY), w-apitest, w-maplibre (Context7-cited, red-first) —
all checked by rerun/mutation. **Boss**: 13 mutations, 13 kills; count-guard caught a live stray; NaN-anchor finding fixed. Corpses = the waste.

## Run 17 — 2026-09-01 — DataSculpt composer: 4-lens review, then 6 fix/test cards

**Job**: relabel a spike result, add Jobard-Lefer streamline placement + schema refines, remove fabricated colour/width defaults, pre-register two tests. **Setup**: constitution 31 lines; cards 15-24 lines; workers tdd-guide sonnet (docs one haiku); checkers haiku (docs) / typescript-reviewer sonnet (code, 4 mutants each); skeptic opus x2. Budget med. **Targeting**: U1 (haiku docs worker delivered on a 15-line card; sonnet code workers delivered) — consistent with L7, still confounded by task class.

| Agent | Band | Card | Result |
|---|---|---|---|
| w-T1 docs | ECONOMY | 2 files / 15 | passed first try |
| w-T4 docs | STANDARD | 2 files / 20 | failed style (3 em dashes) → retry 1 passed |
| w-T2 code | STANDARD | 2 files / 22 (anchors) | passed; retry 1 added 1 test for a survived mutant |
| w-T3 code | STANDARD | 4 files / 24 (anchors) | passed; retry went idle "interrupted" with zero artifacts |
| w-T3b fresh | STANDARD | 2 files / ~30 | passed (3 tests, each RED-proven) |
| w-T5, w-T6 | STANDARD | 4 / 1 files | passed; T5 got two seam edits approved by message |
| skeptic, skeptic2 | FRONTIER | ≤4 attacks | 6 + 4 findings; 2 HIGH on the BOSS-OWNED doc (L43 again) |

**Deaths**: w-T3 retry: card 24 lines, 4 files, redirected yes, retry depth 1, cause **unknown** (idle "interrupted", no transcript checked). Fresh respawn with a boss-rewritten card delivered (L41 first direct observation).

**Worked**: anchor-and-window cards on 400-600-line files (L54) — no reads over budget; local checkpoint commit before mutation (L51); serial mutating checkers with explicit "do NOT run these test files" lines to concurrent workers; skeptic measuring the honesty claim (CV 0.20 vs 0.50) instead of reviewing it; second skeptic pass reproduced the first's number independently.
**Failed**: a worker ran `git stash` to isolate a diff (L15 shape: workers run git); T5's schema change rippled a tsc error into another worker's lane — one fact in two files (L32), resolved by a scoped approval message. Two "PASS" checker verdicts each carried a survived mutant; the boss routed both as retries rather than accepting PASS.
**Confounds**: docs cards are shorter than code cards, so the haiku/sonnet comparison is not controlled.
**Artifacts per token**: 11 files, +29 tests, 15 mutants executed, 2 decision records; STANDARD carried the code, ECONOMY carried docs and mechanical checks; one silent death.
**Documented fixes applied**: L43 (skeptic targets boss-owned files) → yes, found the HIGH. L49 (mutator alone) → yes, no false fails. L51 (commit before mutating) → yes. L41 (fresh respawn) → yes.

## Run 17-18 — 2026-09-02 — Sentinel Phase A (stop-lying) and Phase B round 1
(Phase A stop-lying, 2026-09-02): 3 `tdd-guide` workers + 3 `typescript-reviewer` checkers + 1 skeptic, ZERO deaths (cards 44-60 lines, ≤1 source file; a 403-line seed file was cut from reading lists). Checkers killed 11/12 mutants; survivors were real gaps (freshness shared-grant path; realtime CRLF stall + close race) fixed as retry 1 with their own mutation proofs. Skeptic found one HIGH in a BOSS lane (L43, third time): an honest-failure branch with no test. Policy-file edit deferred until every container-booting worker was idle (containers load policies/*.sql at boot). Confound: `tdd-guide` has no Context7 tools; the worker said so rather than faking a citation. **R18** (Phase B round 1, 2026-09-02): 3 `tdd-guide` workers + 3 checkers + 1 skeptic, zero deaths; one worker STOPPED on a missing workspace dependency instead of hand-symlinking (correct), one caught the card's threshold contradicting decide.ts. Checkers killed 11/14 mutants; 3 survivors were fixture blind spots, fixed as retry 1 with proofs. Skeptic (L43, fourth time) found one CRITICAL and one HIGH in the BOSS adapter lane (orphan verification row on a failed move; actor attribution untested on real Postgres) — the boss adds real-Postgres tests that inspect the table after failure paths. Two gate flakes were 10 s hook timeouts under load → hookTimeout 120 s on container configs.
