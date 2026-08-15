# Call shapes

Copy-paste dispatch patterns. Bands resolve to models via model-intel.md at run time.

## Task card (embed in every worker spawn)

```
TASK CARD #<n>
Objective: <one sentence>
Inputs: <INLINE EXTRACTS — the relevant 20-50 lines pasted in, not paths to big files.
        Reading list ≤2 files + constitution. Same card size for every band.>
Verify yourself with: <narrow scope only, e.g. `vitest run <file>` + `tsc --noEmit`.
        NEVER run the full build — the boss runs it once after all workers finish.>
Done-condition: <testable statement from the spec>
Will be verified by: <exact command/action the checker runs>
Output (return exactly this JSON): {"status": "done|blocked", "evidence": ["..."], "files_touched": ["..."]}
Reporting: when finished, SendMessage this JSON to 'main' — going idle without sending it is an incomplete report.
Mid-task: if blocked, the spec is ambiguous, or constitution clauses conflict, SendMessage 'main' and STOP — never guess.
--- CONSTITUTION ---
<full constitution text>
```

## Agent tool (≤4 tasks, or human review between rounds)

Worker — explicit model, one task, run workers for independent tasks in ONE message:

```
Agent { subagent_type: "general-purpose", model: "haiku",   // ECONOMY worker
        name: "worker-3", description: "Build contact form markup",
        prompt: "<task card #3>" }
```

Checker — CROSS-TIER (different band than the worker), gets card + claim, never the worker's reasoning:

```
Agent { subagent_type: "general-purpose", model: "sonnet",  // STANDARD checker for ECONOMY worker
        name: "checker-3", description: "Verify task 3 by execution",
        prompt: "You are an independent checker. Do NOT trust the worker's report — execute the
        verification yourself (run the command, fetch the page, compare characters). <task card #3>
        Worker claim: <claim JSON>.
        Return: {\"verdict\":\"PASS|FAIL\",\"evidence\":[...],\"repro_command\":\"...\",\"feedback\":\"specific: expected X, got Y\"}" }
```

Specialized checker: reuse an existing agent with the override, e.g.
`Agent { subagent_type: "typescript-reviewer", model: "sonnet", prompt: "<card + diff paths>" }`.

Comms (spawn every agent with `name:` so it stays addressable):
- Retry: SendMessage to the SAME worker by name with the checker's feedback appended.
- Amendment push: SendMessage each affected worker when the boss ratifies a spec/constitution change.
- Missing report: if an agent idles without sending its JSON, SendMessage it once requesting the result; no reply → treat the task as stalled and respawn.
- Workers never message each other — all coordination routes through the boss ('main').

Skeptic — final gate after all tasks PASS (STANDARD, or FRONTIER on --budget high):

```
Agent { subagent_type: "general-purpose", model: "sonnet", name: "skeptic",
        description: "Refute the assembled build",
        prompt: "You are the run's adversarial skeptic. Assume the build is broken; prove it.
        Attack by EXECUTION, not reading: integration seams between tasks, §9 gaming patterns
        (hidden text, hardcoded expectations, disabled/skipped tests, always-valid logic),
        constitution clauses no single checker owned, and the checks themselves.
        Inputs: <constitution path>, <site/build dir>, checker verdicts: <summaries>.
        You are scored on real breaks found, not agreement. Log every attack you ran.
        SendMessage to 'main': {\"verdict\":\"CLEAN|BROKEN\",\"attacks_run\":[...],\"findings\":[{\"task\":n,\"break\":\"...\",\"repro\":\"...\"}]}" }
```

The skeptic reports to 'main' only — it never messages workers and never dispatches its own fixes. The boss adjudicates each finding (skeptics can be wrong; dispute/amendment rules apply), routes accepted ones into the owning task's loop as feedback, and records rejected ones with the reason.

Re-run brief after a fix (always re-run; never accept a fix on the worker's word):

```
SendMessage skeptic: "Re-attack. Changed: <what the worker changed>. Attack priorities:
(1) re-verify the original finding by execution; (2) NEW RISK — the fix added <guard/flag>:
hunt an input path where it swallows a legitimate case (worse than the bug it replaced → CRITICAL);
(3) verify the new tests aren't a mirage — sabotage a scratch copy of the source and confirm the
suite actually goes red; (4) regressions in what previously passed; (5) any constitution amendment
ratified this round, verified by execution."
```

## Workflow tool (5+ tasks, retries, budget)

```js
export const meta = { name: 'foreman-run', description: 'Boss/worker/checker build',
  phases: [{ title: 'Build' }, { title: 'Check' }] }

const CLAIM   = { type:'object', properties:{ status:{type:'string'}, evidence:{type:'array'},
                  files_touched:{type:'array'} }, required:['status','evidence','files_touched'] }
const VERDICT = { type:'object', properties:{ verdict:{enum:['PASS','FAIL']}, evidence:{type:'array'},
                  repro_command:{type:'string'}, feedback:{type:'string'} }, required:['verdict','feedback'] }

// args = { tasks: [{card, workerModel, checkerModel, workerEffort}], constitution }
const results = await pipeline(args.tasks,
  t => agent(t.card + '\n' + args.constitution,
             { model: t.workerModel, effort: t.workerEffort ?? 'medium',
               schema: CLAIM, phase: 'Build', isolation: 'worktree' }),
  async (claim, t) => {                                  // check + retry loop, no barrier
    let feedback = '', last = null
    for (let attempt = 0; attempt < 3; attempt++) {
      const c = claim ?? await agent(t.card + '\nPrior feedback: ' + feedback + '\n' + args.constitution,
                 { model: t.workerModel, schema: CLAIM, phase: 'Build', isolation: 'worktree' })
      last = await agent('Independent checker: EXECUTE the verification, ignore the claim narrative.\n'
                 + t.card + '\nClaim: ' + JSON.stringify(c),
                 { model: t.checkerModel, schema: VERDICT, phase: 'Check' })
      if (last.verdict === 'PASS') return { task: t.card.slice(0, 60), ...last, attempts: attempt + 1 }
      feedback = last.feedback; claim = null              // retry same band with specifics
    }
    return { task: t.card.slice(0, 60), ...last, escalate: true }  // boss decides in-session
  })
return { results: results.filter(Boolean) }
```

Budget guard: `while (budget.total && budget.remaining() < 50_000) break` before spawning extra rounds.
Resume after edits: `Workflow({ scriptPath, resumeFromRunId })` — unchanged agent() calls return cached.

## Discovery probes

```bash
# API roster (optional, needs key)
curl -s https://api.anthropic.com/v1/models -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" | python3 -c "import json,sys; [print(m['id']) for m in json.load(sys.stdin)['data']]"
# Pinned models across the local agent fleet
grep -h '^model:' ~/.claude/agents/*.md | sort | uniq -c
```
