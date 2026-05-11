# Integrations

DoneSpec works with coding agents and CI systems because it is a local deterministic CLI.

It does not run inside the agent. It does not add an agent runtime, API key, cloud service, database, dashboard, memory layer, or LLM dependency.

The integration point is the command:

```bash
donespec validate done.json --strict
```

## Agent completion instruction

Paste this into agent instructions, project rules, or task prompts:

```text
You may only claim completion after:

1. implementing the requested change
2. running the project's normal checks
3. running `donespec validate done.json --strict`
4. fixing any failures
5. reporting the final validation result

Do not weaken, remove, or bypass DoneSpec checks to make validation pass.
```

DoneSpec does not replace review, tests, or judgement. It verifies the explicit completion contract before an agent claims the task is done.

## Codex

Use `AGENTS.md` for repository-level Codex instructions.

Copy-paste instruction:

```text
Before claiming the task is complete, run:

donespec validate done.json --strict

If validation fails, fix the issue and run it again.
Do not mark the task complete until DoneSpec passes.
Do not weaken, remove, or bypass DoneSpec checks to make validation pass.
```

Recommended workflow:

```bash
donespec explain done.json --strict
donespec validate done.json --strict
```

## Claude Code

Use `CLAUDE.md` to import the shared repository rules from `AGENTS.md`.

Claude Code should:

1. read the task contract in `done.json`
2. make the requested change
3. run the project's normal tests or checks
4. run `donespec validate done.json --strict`
5. report failures honestly and continue fixing until validation passes

Copy-paste instruction:

```text
Read the DoneSpec contract before editing.
Run the project checks after editing.
Run `donespec validate done.json --strict` before reporting completion.
If validation fails, report the failing check and fix the underlying issue.
Do not weaken done.json checks unless the human explicitly asks for a contract change.
```

## Cursor

Cursor can use DoneSpec through normal VS Code-style project files and terminal tasks.

Recommended setup:

- keep `done.json` in the project root
- associate `done.json` with `done.schema.json`
- run DoneSpec from the integrated terminal or a task
- ask Cursor agents to validate before completion

Copy-paste project rule:

```text
This repository uses DoneSpec for deterministic completion validation.

Before marking a task as done, run:

donespec validate done.json --strict

If validation fails, continue working until it passes.
Do not remove, weaken, or bypass checks in done.json unless explicitly requested.
```

## Aider

Use DoneSpec as the validation step after Aider modifies files.

Simple workflow:

```bash
aider --message "Make the requested change. Keep done.json visible. Before reporting completion, run donespec validate done.json --strict and fix any failures."
```

Copy-paste instruction:

```text
The project uses DoneSpec.

After modifying files, run:

donespec validate done.json --strict

Do not accept conversational completion without validation.
Do not edit done.json to bypass the intended contract.
```

## OpenAI Agents SDK

Keep DoneSpec as an external deterministic validation command in the workflow.

Do not build DoneSpec into a runtime integration. The agent workflow only needs to call the CLI after modifications.

Copy-paste instruction:

```text
After applying code changes, execute:

donespec validate done.json --strict

Return success only if the command exits with code 0.
If it exits non-zero, treat the task as incomplete and inspect the failure output.
Do not weaken, remove, or bypass DoneSpec checks to make validation pass.
```

Conceptual flow:

```text
agent edits files
agent runs project checks
agent runs DoneSpec
DoneSpec returns an exit code
agent reports only if validation passed
```

## GitHub Actions

Use the DoneSpec action to install the CLI, then run strict validation explicitly:

```yaml
name: DoneSpec

on:
  pull_request:
  push:

jobs:
  donespec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: xryv/DoneSpec@v0.8.0
      - name: Validate completion contract
        run: donespec validate done.json --strict
```

This keeps the workflow copy-paste ready while preserving strict mode as the visible CI gate.

## Generic CI pipeline

Any CI system can run DoneSpec as a normal command:

```bash
pip install donespec
donespec validate done.json --strict
```

Recommended stage order:

```text
install dependencies
run tests
run DoneSpec validation
publish only if DoneSpec passes
```

## What not to do

- Do not treat a conversational agent summary as completion.
- Do not weaken, remove, or bypass DoneSpec checks to make validation pass.
- Do not hide failures behind CI-only configuration.
- Do not turn DoneSpec into an agent runtime or orchestration layer.
- Do not skip tests or review because DoneSpec passed.

DoneSpec verifies explicit contracts. It does not guarantee correctness, replace CI, or replace human review.
