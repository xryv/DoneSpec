# Editor support

DoneSpec contracts are plain JSON. Editors can validate and autocomplete `done.json` before the CLI runs.

The recommended local files are:

```text
done.json
done.schema.json
```

Generate the schema with:

```bash
donespec schema --write done.schema.json
```

Projects created with `donespec init` already include both files.

## VS Code schema association

Create or update:

```text
.vscode/settings.json
```

with:

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

This maps:

```text
done.json -> done.schema.json
```

VS Code can then provide validation, autocomplete, type hints, missing-field warnings, and unsupported-field warnings.

## Cursor compatibility

Cursor uses VS Code-style workspace settings.

Use the same `.vscode/settings.json` schema association:

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

## Other editors

Any editor with JSON Schema support can use the same local mapping:

```text
done.json -> done.schema.json
```

No editor extension, cloud service, or network access is required.

This keeps schema support local-first.

## Why autocomplete matters

Autocomplete makes reliable contracts easier to author.

It helps humans and coding agents see:

- supported check types
- required fields
- optional fields
- `must_pass` and `must_not` group structure
- `version` and `task_id`
- unsupported properties before validation

The editor helps write the contract. The CLI enforces it:

```bash
donespec validate done.json --strict
```
