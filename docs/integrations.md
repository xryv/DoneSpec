# Integrations

DoneSpec works with any coding agent or CI system because it is just a local deterministic CLI.

There is no API key, cloud service, agent runtime, database, dashboard, memory layer, or LLM dependency.

The universal integration rule is:

```text
Before claiming completion, run:

donespec validate done.json --strict

If validation fails, the task is not complete.
Do not weaken done.json to make validation pass unless explicitly requested by the human.
```

## Codex

Add this to your agent instructions:

```text
Use DoneSpec as the final completion gate.

Before saying the task is complete:

1. Run `donespec explain done.json --strict` to inspect the contract.
2. Perform the requested work.
3. Run `donespec validate done.json --strict`.
4. If validation fails, fix the implementation and run validation again.
5. Do not modify `done.json` only to make validation easier unless explicitly instructed.
```

Recommended final command:

```bash
donespec validate done.json --strict
```

## Claude Code

Add this to `CLAUDE.md`:

```text
@AGENTS.md

Before reporting completion, run:

donespec validate done.json --strict

If DoneSpec fails, the work is not complete.
Never weaken the DoneSpec contract unless the human explicitly asks for a contract change.
```

Recommended workflow:

```bash
donespec explain done.json --strict
donespec validate done.json --strict
```

## Cursor

Add this to Cursor project rules:

```text
This repository uses DoneSpec for deterministic completion validation.

Before marking a task as done, run:

donespec validate done.json --strict

If validation fails, continue working until it passes.
Do not remove or weaken checks in done.json unless explicitly requested.
```

Useful terminal command:

```bash
donespec validate done.json --strict
```

## Aider

Add this to your Aider instruction file or project prompt:

```text
The project uses DoneSpec.

At the end of every task, run:

donespec validate done.json --strict

If validation fails, inspect the failure, fix the issue, and rerun validation.
Do not edit done.json to bypass the intended contract.
```

Recommended command:

```bash
aider --message "Complete the task, then run donespec validate done.json --strict before reporting done."
```

## OpenAI Agents SDK

Use DoneSpec as a deterministic terminal gate after agent execution.

Example instruction:

```text
After applying code changes, execute:

donespec validate done.json --strict

Return success only if the command exits with code 0.
If it exits non-zero, treat the task as incomplete and inspect the failure output.
```

Conceptual flow:

```text
agent edits files
  ↓
agent runs DoneSpec
  ↓
DoneSpec returns exit code
  ↓
agent reports only if validation passed
```

## GitHub Actions

Use DoneSpec in CI:

```yaml
name: DoneSpec

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: xryv/DoneSpec@v0.8.0

      - name: Validate completion contract
        run: donespec validate done.json --strict
```

## Generic CI pipeline

Any CI system can run:

```bash
pip install donespec
donespec validate done.json --strict
```

Recommended pipeline stage:

```text
install dependencies
run tests
run DoneSpec validation
publish only if DoneSpec passes
```

## Local shell workflow

For humans:

```bash
donespec explain done.json --strict
donespec validate done.json --strict
```

For agents:

```bash
donespec validate done.json --strict
```

For machine-readable output:

```bash
donespec validate done.json --strict --json
```

## Pre-push workflow

Install generated hooks:

```bash
donespec init --yes
```

Then install git hooks:

Windows PowerShell:

```powershell
.\scripts\install-git-hooks.ps1
```

Unix:

```bash
./scripts/install-git-hooks.sh
```

This blocks pushes when the completion contract fails.

## Recommended agent contract

Use this minimal instruction for any agent:

```text
You may modify the repository to complete the task.

Completion is valid only when:

donespec validate done.json --strict

passes with exit code 0.

Do not claim completion before this command passes.
Do not weaken the contract unless explicitly asked.
```

## Philosophy

DoneSpec integrates well because it does almost nothing magical.

It defines a contract.

It runs deterministic checks.

It returns an exit code.

That is enough.
