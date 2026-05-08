# `donespec validate --strict`

`donespec validate --strict` enables semantic validation for `done.json`.

The normal validator already checks that `done.json` is valid JSON and matches the DoneSpec JSON Schema.

Strict mode goes further.

It checks whether the contract is safe, deterministic, and suitable for AI coding agents, multi-agent workflows, and CI enforcement.

## Run

```bash
donespec validate done.json --strict
```

## Why strict mode exists

JSON Schema validates the structure of the contract.

Strict mode validates the quality of the contract.

A `done.json` file can be structurally valid but still weak, ambiguous, or unsafe for automation.

For example:

- duplicate check names
- duplicate check IDs
- invalid regex patterns
- absolute paths
- parent traversal paths
- empty validation contracts
- unnamed checks

Strict mode catches these problems before execution.

In other words, strict mode helps detect unsafe paths, ambiguous checks, weak contracts, and malformed validation rules before any task is considered complete.

## What strict mode checks

Strict mode currently validates:

```text
✓ done.json contains at least one check
✓ every check has a non-empty name
✓ check names are unique
✓ check IDs are unique when provided
✓ regex patterns compile correctly
✓ file paths are relative
✓ file paths do not contain ..
```

## Normal validation

```bash
donespec validate done.json
```

Normal validation:

- loads `done.json`
- validates it against the JSON Schema
- executes the declared checks
- reports pass/fail results

## Strict validation

```bash
donespec validate done.json --strict
```

Strict validation:

- loads `done.json`
- validates it against the JSON Schema
- validates semantic contract quality
- executes the declared checks only if strict validation passes

## Example failure: duplicate names

Invalid:

```json
{
  "version": "1.0",
  "task_id": "example",
  "must_pass": [
    {
      "type": "file_exists",
      "name": "README exists",
      "path": "README.md"
    },
    {
      "type": "file_exists",
      "name": "README exists",
      "path": "docs/index.md"
    }
  ],
  "must_not": []
}
```

Run:

```bash
donespec validate done.json --strict
```

Expected failure:

```text
Spec error: Strict validation failed:
- duplicate check name: 'README exists'
```

## Example failure: invalid regex

Invalid:

```json
{
  "version": "1.0",
  "task_id": "example",
  "must_pass": [
    {
      "type": "regex_in_file",
      "name": "README has invalid regex",
      "path": "README.md",
      "pattern": "["
    }
  ],
  "must_not": []
}
```

Expected failure:

```text
Spec error: Strict validation failed:
- must_pass[0] regex pattern is invalid
```

## Example failure: unsafe path

Invalid:

```json
{
  "version": "1.0",
  "task_id": "example",
  "must_pass": [
    {
      "type": "file_exists",
      "name": "Outside project",
      "path": "../README.md"
    }
  ],
  "must_not": []
}
```

Expected failure:

```text
Spec error: Strict validation failed:
- must_pass[0] path must not contain '..'
```

## Recommended agent instruction

For agentic coding workflows, use this rule:

```text
Before claiming completion, run:

donespec validate done.json --strict

If strict validation fails, the task is not complete.
Do not weaken done.json to make validation pass unless the human explicitly changes the contract.
```

## Recommended CI usage

For stricter CI enforcement:

```yaml
- run: donespec validate done.json --strict
```

This is useful when DoneSpec is used as a hard completion gate for AI-generated changes.

## When to use strict mode

Use strict mode for:

- public repositories
- agent-generated pull requests
- multi-agent workflows
- CI enforcement
- reusable templates
- production tasks
- swarm-based coding workflows

Normal validation remains useful for quick local checks.

Strict validation is recommended when the contract itself must be trustworthy.

## Philosophy

Normal validation answers:

```text
Did the declared checks pass?
```

Strict validation answers:

```text
Is this completion contract safe enough to trust?
```

Done still means:

```bash
donespec validate done.json
```

But for serious agent workflows, the stronger gate is:

```bash
donespec validate done.json --strict
```
