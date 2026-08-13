# Model intel (living document)

last-verified: 2026-08-13
refresh-rule: if >30 days old, or discovery finds an uncovered model, re-research (WebSearch: pricing, coding benchmarks, context limits) and rewrite this table with a new date.

| Model | ID | Band | $/Mtok in/out | Notes |
|---|---|---|---|---|
| Fable 5 | claude-fable-5 | FRONTIER | 10 / 50 | Most capable GA model; Mythos-class tier above Opus. Boss/arbitration only — never a worker. |
| Opus 5 | claude-opus-5 | FRONTIER | 5 / 25 | Deep reasoning; boss when Fable unavailable, or final-review checker. |
| Sonnet 5 | claude-sonnet-5 | STANDARD | 2 / 10 (intro to 2026-08-31, then 3 / 15) | Default implementation worker and logic checker. |
| Haiku 4.5 | claude-haiku-4-5-20251001 | ECONOMY | 1 / 5 | Mechanical work, boilerplate, copy, compare-checks, research fan-out. ~90% of Sonnet capability at 1/3 cost. |

Discounts that change routing math: cache hits = 10% of input price; Batch API = 50% off (stacks with caching). Claude 4.7+ tokenizer emits ~30% more tokens for the same text — factor into cross-generation comparisons.

Effort multiplier (Workflow `agent()` only): `effort: high|xhigh` on a STANDARD model is often cheaper AND better than a lazy FRONTIER call for well-specified tasks; `effort: low` on ECONOMY for pure-mechanical.

Sources (2026-08): finout.io, cloudzero.com, benchlm.ai, aipricing.guru Anthropic pricing guides.
