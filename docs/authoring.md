# `donespec add-check`

`donespec add-check` safely adds checks to an existing `done.json`.

It is the first command in the DoneSpec Contract Authoring Layer.

The goal is simple:

```text
Agents should not need to invent done.json by hand.
```

Instead of manually editing JSON, agents and humans can use a structured command that validates the contract before writing it.

## Basic usage

```bash
donespec add-check done.json --type file_exists --name "README exists" --path README.md
```

This adds:

```json
{
  "type": "file_exists",
  "name": "README exists",
  "path": "README.md"
}
```

to `must_pass`.

## Why this exists

Manual contract editing is fragile.

AI coding agents can easily:

- invent unsupported fields
- duplicate check names
- create unsafe paths
- write invalid regex patterns
- add checks to the wrong group
- create structurally valid but semantically weak contracts

`donespec add-check` reduces that risk.

After building the new check, DoneSpec validates the updated contract through:

```text
JSON Schema validation
Strict semantic validation
```

Only then is `done.json` written.

## Add a command check

```bash
donespec add-check done.json \
  --type command \
  --name "pytest passes" \
  --run "pytest -q"
```

Optional command fields:

```bash
--expected-exit-code 0
--timeout-seconds 120
```

## Add a file check

```bash
donespec add-check done.json \
  --type file_exists \
  --name "README exists" \
  --path README.md
```

## Add a regex check

```bash
donespec add-check done.json \
  --type regex_in_file \
  --name "README contains philosophy" \
  --path README.md \
  --pattern "Done means deterministically verified"
```

With flags:

```bash
donespec add-check done.json \
  --type regex_in_file \
  --name "README has title" \
  --path README.md \
  --pattern "^#" \
  --flag MULTILINE
```

Supported regex flags:

```text
IGNORECASE
MULTILINE
DOTALL
```

## Add a forbidden regex check

```bash
donespec add-check done.json \
  --group must_not \
  --type regex_absent \
  --name "No secret keys" \
  --path README.md \
  --pattern "SECRET_KEY"
```

## Add a file-not-modified check

```bash
donespec add-check done.json \
  --group must_not \
  --type file_not_modified \
  --name "README untouched" \
  --path README.md
```

## Add an HTTP check

```bash
donespec add-check done.json \
  --type http_check \
  --name "health endpoint responds" \
  --url "http://127.0.0.1:8000/health"
```

Optional HTTP fields:

```bash
--method GET
--expected-status 200
--timeout-seconds 10
--headers-json "{\"Accept\":\"application/json\"}"
```

## Target groups

Default group:

```text
must_pass
```

Explicit group:

```bash
donespec add-check done.json --group must_not ...
```

Supported groups:

```text
must_pass
must_not
```

## Safety rules

`donespec add-check` rejects contracts that would fail strict validation.

It catches:

```text
duplicate check names
duplicate check IDs
invalid regex patterns
absolute paths
parent traversal paths
empty or malformed checks
unsupported check types
missing required fields
```

## Recommended workflow

For agents:

```bash
donespec explain done.json
donespec add-check done.json --type file_exists --name "README exists" --path README.md
donespec validate done.json --strict
```

For humans:

```bash
donespec add-check done.json --type command --name "tests pass" --run "pytest -q"
donespec validate done.json --strict
```

## Philosophy

`donespec validate` answers:

```text
Did the contract pass?
```

`donespec explain` answers:

```text
What does the contract require?
```

`donespec add-check` answers:

```text
Can this contract be safely extended?
```

This is the beginning of DoneSpec as a deterministic authoring protocol for AI agents.
