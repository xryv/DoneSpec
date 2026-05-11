# `done.json` schema

`done.json` is the DoneSpec completion contract.

It is a small JSON document that declares the deterministic checks required before a task can be considered complete. The schema defines the shape of that contract so editors, CI, agents, and humans can inspect the same file before execution.

The schema validates structure. The validator executes checks.

```bash
donespec schema
donespec schema --write done.schema.json
donespec validate done.json
```

## Top-level structure

A DoneSpec file has a stable top-level shape:

```json
{
  "$schema": "done.schema.json",
  "version": "1.0",
  "task_id": "ship-safe-change",
  "description": "Optional human-readable context.",
  "must_pass": [],
  "must_not": []
}
```

Fields:

- `$schema`: optional local schema reference for editors and tools.
- `version`: schema version. For v1, this is `"1.0"`.
- `task_id`: stable identifier for the contract. It must be non-empty and use letters, numbers, dots, underscores, colons, or hyphens.
- `description`: optional human-readable context.
- `must_pass`: checks that must pass.
- `must_not`: checks that protect against forbidden states or changes.

At least one of `must_pass` or `must_not` must be present.

## Check object structure

Every check has a `type`. Checks may also define:

- `id`: optional stable check identifier.
- `name`: optional in normal validation, required by strict mode.

Supported check types:

| Type                | Required fields       | Optional fields                                      |
| ------------------- | --------------------- | ---------------------------------------------------- |
| `command`           | `type`, `run`         | `name`, `id`, `expected_exit_code`, `timeout_seconds` |
| `file_exists`       | `type`, `path`        | `name`, `id`                                        |
| `regex_in_file`     | `type`, `path`, `pattern` | `name`, `id`, `flags`                           |
| `regex_absent`      | `type`, `path`, `pattern` | `name`, `id`, `flags`                           |
| `file_not_modified` | `type`, `path`        | `name`, `id`                                        |
| `http_check`        | `type`, `url`         | `name`, `id`, `method`, `expected_status`, `timeout_seconds`, `headers` |

Group names are fixed:

```json
{
  "must_pass": [],
  "must_not": []
}
```

Do not invent new groups or check types. Unknown fields are rejected by the JSON Schema.

## Minimal realistic contract

```json
{
  "$schema": "done.schema.json",
  "version": "1.0",
  "task_id": "docs-change",
  "must_pass": [
    {
      "type": "file_exists",
      "name": "README exists",
      "path": "README.md"
    },
    {
      "type": "regex_in_file",
      "name": "README contains positioning",
      "path": "README.md",
      "pattern": "deterministic completion layer"
    }
  ],
  "must_not": [
    {
      "type": "file_not_modified",
      "name": "lockfile untouched",
      "path": "uv.lock"
    }
  ]
}
```

## JSON Schema usage

Print the packaged schema:

```bash
donespec schema
```

Write it locally:

```bash
donespec schema --write done.schema.json
```

Overwrite an existing schema file:

```bash
donespec schema --write done.schema.json --force
```

New projects initialized with:

```bash
donespec init --yes
```

include:

```text
done.json
done.schema.json
```

## Editor autocomplete

Use the local schema file to give editors validation and autocomplete:

```json
{
  "json.schemas": [
    {
      "fileMatch": [
        "/done.json"
      ],
      "url": "./done.schema.json"
    }
  ]
}
```

This helps authors see supported check types, required fields, optional fields, and unsupported properties before the CLI runs.

See [editor-support.md](editor-support.md).

## Strict mode relationship

JSON Schema validates the contract shape.

Strict mode validates contract hygiene:

```bash
donespec validate done.json --strict
```

Strict mode catches cases that are structurally valid but unsafe or ambiguous for automation, including:

- empty contracts
- unnamed checks
- duplicate check names
- duplicate check IDs
- invalid regex patterns
- absolute paths
- parent traversal paths

See [strict.md](strict.md).

## CI usage

Use the same local contract in CI:

```yaml
- run: donespec validate done.json --strict
```

No remote schema fetch is required when `done.schema.json` is checked into the repository.

## v1 schema stability

DoneSpec v1 treats `done.json` as a stable contract format.

- v1 changes should be additive where possible.
- Existing valid v1 specs should not break without a strong reason.
- Strict mode may reject unsafe or ambiguous specs.
- The schema is local-first and does not require network access.
- The format is intended to be readable by humans, editors, CI systems, and coding agents.

This stability is what lets `done.json` behave like infrastructure: boring, explicit, and repeatable.

## Compatibility expectations

For v1:

- field names remain stable
- check type names remain stable
- `must_pass` and `must_not` remain the only check groups
- `version` remains `"1.0"`
- JSON output and human output remain separate concerns
- schema validation remains structural
- strict validation remains semantic hygiene

DoneSpec should remain small enough that the contract can be understood by reading one JSON file.
