# `donespec schema`

`donespec schema` prints or writes the official DoneSpec JSON Schema.

It exists to make `done.json` easier to validate, edit, autocomplete, and integrate with tools.

The core command is:

```bash
donespec schema
```

Write the schema to a local file:

```bash
donespec schema --write done.schema.json
```

Overwrite an existing schema file:

```bash
donespec schema --write done.schema.json --force
```

## Why this exists

DoneSpec is designed to become a deterministic completion contract for AI coding agents.

For that contract to become portable across editors, agents, CI systems, and automation tools, the shape of `done.json` must be machine-readable.

The JSON Schema allows:

- editor validation
- autocomplete
- safer manual editing
- CI validation
- agent-side contract inspection
- integration with external tools
- deterministic validation before execution

## Generated schema reference

New projects initialized with:

```bash
donespec init --yes
```

now generate:

```text
done.json
done.schema.json
```

The generated `done.json` includes:

```json
{
  "$schema": "done.schema.json",
  "version": "1.0",
  "task_id": "generic-validation",
  "must_pass": [],
  "must_not": []
}
```

## Print schema

To print the packaged schema:

```bash
donespec schema
```

This writes the JSON Schema to stdout.

Useful for:

```bash
donespec schema | python -m json.tool
```

## Write schema

To write the schema to a project:

```bash
donespec schema --write done.schema.json
```

If the file already exists, DoneSpec will not overwrite it by default.

Use:

```bash
donespec schema --write done.schema.json --force
```

to overwrite the existing file.

## Recommended workflow

For a new project:

```bash
pip install donespec
donespec init --template python --yes
donespec validate done.json
```

This creates both:

```text
done.json
done.schema.json
```

For an existing project:

```bash
donespec schema --write done.schema.json
```

Then add this to `done.json`:

```json
{
  "$schema": "done.schema.json"
}
```

## Agent workflow

AI coding agents should treat the schema as the structural contract for `done.json`.

Recommended instruction:

```text
Before editing done.json, inspect done.schema.json.
Do not invent unsupported check fields.
Do not remove deterministic checks unless explicitly requested.
Before claiming completion, run donespec validate done.json.
```

## Philosophy

`donespec schema` does not validate task completion.

That remains the job of:

```bash
donespec validate done.json
```

The schema validates the shape of the contract.

The validator executes the contract.
