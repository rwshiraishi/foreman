# Lessons ledger (living document)

Lifecycle and promotion rules: `run-retro.md`. Read this BEFORE writing any spec.
Statuses: CANDIDATE → PROMOTED (or DEMOTED). UNANSWERED questions listed at bottom.

## L1 — boss-extracts-inline-inputs — PROMOTED
- **Rule**: The boss puts the relevant 20-50 lines IN the task card; workers never
  read large sources. Reading list ≤2 files + constitution.
- **Evidence**: Run 1 (2026-08-14, marketing page port): 3 of 3 deaths were
  autocompact thrash, all three cards listed 8-10 files; both survivors had ~3-file
  cards. Airtight causal chain (identical failure reason, self-reported).
- **Landed-in**: SKILL.md §6 "Context budget"; call-shapes.md task card.

## L2 — no-concurrent-full-builds — PROMOTED
- **Rule**: Worker/checker verification is single-file test + typecheck only; the
  full build is boss-only, once, after all workers finish (or per-worker worktrees).
- **Evidence**: Run 1: two concurrent `pnpm run build` corrupted `.next`
  (`ENOENT .nft.json`), producing false FAILs misdiagnosed as disk failure.
- **Landed-in**: SKILL.md §6 "Verification scope"; constitution-template.md
  verification commands; call-shapes.md task card.

## L3 — card-size-constant-across-bands — PROMOTED
- **Rule**: Task card size must not vary with model band; coupling them makes the
  run uninterpretable.
- **Evidence**: Run 1 confound: "harder" tasks got both higher band AND longer
  reading list, so band reliability could not be judged.
- **Landed-in**: SKILL.md §6 "Context budget".

## L4 — filesystem-is-the-report — PROMOTED
- **Rule**: Assume the report may never arrive; verify work via `git status` /
  expected outputs. Withhold root-cause judgment until the idle notification lands.
- **Evidence**: Run 1: dead agents left no transcript, ignored pings; real cause
  arrived late via idle notifications after a wrong disk-failure diagnosis.
- **Landed-in**: SKILL.md §6 comms contract; §9 silent-agent row.

## L5 — artifacts-per-token-metric — PROMOTED
- **Rule**: Judge runs by delivered artifacts per token, not agents spawned.
- **Evidence**: Run 1: 3 dead STANDARD agents dominated spend; 2 ECONOMY workers
  delivered everything.
- **Landed-in**: SKILL.md §8.

## L6 — content-inventory-diff — PROMOTED
- **Rule**: For restyle/port tasks, diff the content inventory (titles/sections)
  before vs after — cheap, high-signal proof nothing was dropped.
- **Evidence**: Run 1 "what worked".
- **Landed-in**: constitution-template.md content-task verification.

## L7 — economy-tier-does-real-work — CANDIDATE
- **Rule (provisional)**: ECONOMY (haiku) handles full page builds with substantive
  tests when the card is well-extracted; don't reflexively band-up page work.
- **Evidence**: Run 1: both haiku workers passed with real assertions. Only one
  run; entangled with the L3 confound (they also had the small cards).
- **Needs**: one more run with constant card sizes.

## UNANSWERED
- **U1**: Is STANDARD (sonnet) less reliable than ECONOMY under identical cards, or
  was Run 1's death rate purely card size? Settle with a controlled run: same card
  size across bands (Run 1, 2026-08-14).
