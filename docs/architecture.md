# Architecture

DoneSpec is intentionally small.

```text
done.json -> loader -> JSON schema validation -> validation engine -> checker registry -> checkers -> report -> CLI output
```

## Modules

- `cli.py` owns command-line UX and exit codes.
- `loader.py` reads and validates `done.json`.
- `schema.py` loads the packaged JSON Schema.
- `engine.py` executes checks in deterministic order.
- `models.py` defines structured result and report objects.
- `checkers/registry.py` maps `type` values to checker classes.
- `checkers/*` contains isolated deterministic validators.

## Checker contract

Every checker receives:

- raw check config,
- check group: `must_pass` or `must_not`,
- validation context: project root and spec path.

Every checker returns:

- `passed`,
- `duration_ms`,
- `error`,
- `details`,
- `metadata`.

Checkers should not print. They should only return structured data.

## Why no AI in the core?

DoneSpec is a deterministic boundary. AI agents can generate code and even draft `done.json`, but final completion must be validated by reproducible checks.

## Future extension points

The current architecture leaves room for:

- MCP server integration,
- AI-agent handoff integrations,
- generated `done.json`,
- VSCode extension,
- multi-agent validation flows,
- hosted analytics.

These are intentionally outside the MVP.
