# Model Route

Dispatch the task through the foreman skill (tiered boss/worker/checker orchestration).

## Usage

`/model-route [task-description] [--budget low|med|high]`

## Behavior

1. Invoke the `foreman` skill.
2. If the task is below foreman's decomposition threshold (≤2 files, <100 lines, or <3 verifiable tasks): output a one-line band recommendation (ECONOMY/STANDARD/FRONTIER with the concrete model from foreman's model-intel table) and stop — spawn nothing.
3. Otherwise run the full pattern: model discovery → constitution → tiered dispatch with task cards → independent checker loop → cost report.
4. `--budget low` caps workers at ECONOMY and checkers at STANDARD; `--budget high` permits FRONTIER arbitration rounds. Default `med`.

## Arguments

$ARGUMENTS: `[task-description]` optional free-text; `--budget low|med|high` optional.
