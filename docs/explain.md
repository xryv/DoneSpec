# `donespec explain`

`donespec explain` explains a DoneSpec contract without executing checks.

It exists to help humans, AI coding agents, CI systems, and agent swarms understand what `done.json` requires before they begin work.

## Run

```bash
donespec explain done.json
```

Machine-readable output:

```bash
donespec explain done.json --json
```

Strict semantic validation before explaining:

```bash
donespec explain done.json --strict
```

## Why this exists

DoneSpec is a deterministic completion contract.

Before an agent changes code, it should understand:

- what task contract it is working against,
- how many checks exist,
- which checks are required,
- which checks are forbidden,
- which commands will be executed,
- which files are protected,
- which regex rules are enforced,
- which gate should be used before declaring completion.

`donespec explain` gives that overview without running the task checks.

## Human-readable output

Example:

```text
DoneSpec explanation: python-validation

Version: 1.0
Total checks: 4

Groups:
- must_pass: 4
- must_not: 0

Check types:
- command: 3
- file_exists: 1

Must pass:
✓ 1. [file_exists] DoneSpec file exists
   path: done.json
✓ 2. [command] ruff lint passes
   run: ruff check .

Recommended gate:
donespec validate done.json --strict
```

## JSON output

```bash
donespec explain done.json --json
```

Example shape:

```json
{
  "spec_path": "/path/to/done.json",
  "schema": "done.schema.json",
  "version": "1.0",
  "task_id": "python-validation",
  "description": null,
  "total_checks": 4,
  "groups": {
    "must_pass": 4,
    "must_not": 0
  },
  "types": {
    "command": 3,
    "file_exists": 1
  },
  "checks": [
    {
      "group": "must_pass",
      "index": 0,
      "id": null,
      "name": "DoneSpec file exists",
      "type": "file_exists",
      "details": {
        "path": "done.json"
      }
    }
  ],
  "recommended_gate": "donespec validate done.json --strict"
}
```

## Agent workflow

Recommended instruction for agents:

```text
Before starting work, run:

donespec explain done.json

Then inspect the required checks.

Before claiming completion, run:

donespec validate done.json --strict
```

## Swarm workflow

In a multi-agent workflow, `donespec explain --json` can be used as a shared contract snapshot.

Planner agents can use it to assign work.

Worker agents can use it to understand what must pass.

Reviewer agents can use it to verify that the declared contract was not weakened.

CI can use it to expose the contract in logs without executing checks.

## Difference from validate

`explain` answers:

```text
What does this contract require?
```

`validate` answers:

```text
Did the contract pass?
```

For completion enforcement, the final gate remains:

```bash
donespec validate done.json --strict
```

## Philosophy

Agents should not blindly execute a contract they do not understand.

`donespec explain` makes the contract inspectable before it becomes enforceable.
