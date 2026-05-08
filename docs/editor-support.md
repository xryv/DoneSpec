# Editor support

DoneSpec contracts are plain JSON.

That means `done.json` can be validated, inspected, and completed by editors before the CLI ever runs.

The goal is simple:

```text
done.json should feel like a real infrastructure file.
```

Similar to:

```text
package.json
pyproject.toml
openapi.json
tsconfig.json
```

## Generated schema

Every initialized DoneSpec project includes:

```text
done.json
done.schema.json
```

The schema can also be exported manually:

```bash
donespec schema --write done.schema.json
```

## VS Code schema association

To enable validation and autocomplete in VS Code, create or update:

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

Now VS Code can provide:

- field validation
- autocomplete
- type hints
- missing-field warnings
- unsupported-field warnings

## Cursor schema association

Cursor uses VS Code-compatible workspace settings.

Use the same file:

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

This helps both humans and agents understand the contract shape before execution.

## Generic editor support

Any editor that supports JSON Schema can associate:

```text
done.json -> done.schema.json
```

Recommended local files:

```text
done.json
done.schema.json
```

Recommended validation gate:

```bash
donespec validate done.json --strict
```

## Agent benefit

Editor schema support helps AI coding agents because the contract becomes easier to inspect.

Agents can read:

```text
done.json
done.schema.json
```

and infer:

- allowed check types
- required fields
- optional fields
- check group structure
- schema version
- strict validation expectations

This reduces malformed contracts.

## Recommended workspace files

A well-prepared project can include:

```text
done.json
done.schema.json
AGENTS.md
CLAUDE.md
.vscode/tasks.json
.vscode/settings.json
.githooks/pre-push
scripts/install-git-hooks.ps1
scripts/install-git-hooks.sh
```

DoneSpec remains local-first.

No editor extension is required.

No cloud service is required.

No agent runtime is required.

## Philosophy

The schema is part of the trust layer.

The CLI enforces the contract.

The editor helps authors write the contract correctly.

Together they make completion explicit, inspectable, and deterministic.
