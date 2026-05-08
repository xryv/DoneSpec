# `donespec templates`

DoneSpec templates provide starter `done.json` contracts for common project types.

They exist to answer one practical question:

```text
What should my first done.json contain?
```

Instead of starting from an empty validation contract, use:

```bash
donespec init --template python --yes
```

## List templates

```bash
donespec templates
```

Machine-readable output:

```bash
donespec templates --json
```

## Available templates

### `generic`

```bash
donespec init --template generic --yes
```

A minimal universal DoneSpec contract.

Best for:

- unknown project types,
- early experiments,
- generic agent workflows,
- repositories where custom checks will be added manually.

### `python`

```bash
donespec init --template python --yes
```

Creates checks for:

- Python availability,
- Ruff linting,
- Ruff format check,
- pytest.

Best for:

- Python packages,
- CLI tools,
- backend services,
- automation scripts,
- agent-generated Python code.

### `node`

```bash
donespec init --template node --yes
```

Creates checks for:

- `package.json`,
- `npm test`,
- `npm run build`.

Best for:

- Node.js projects,
- TypeScript projects,
- frontend apps,
- JavaScript libraries,
- agent-generated web code.

### `docs`

```bash
donespec init --template docs --yes
```

Creates checks for:

- `README.md`,
- README title presence.

Best for:

- documentation tasks,
- README rewrites,
- release documentation,
- docs-only pull requests.

### `api`

```bash
donespec init --template api --yes
```

Creates an example runtime check for:

```text
http://127.0.0.1:8000/health
```

Best for:

- local API services,
- backend health checks,
- runtime validation,
- agent-generated services.

The URL is intentionally a starter example. Adjust it to match your project.

## Recommended usage

For a Python project:

```bash
pip install donespec
donespec init --template python --yes
donespec validate done.json
```

For a Node project:

```bash
pip install donespec
donespec init --template node --yes
donespec validate done.json
```

For a documentation task:

```bash
pip install donespec
donespec init --template docs --yes
donespec validate done.json
```

## Agent workflow

Templates are especially useful for AI coding agents because they create immediate deterministic expectations.

Example:

```bash
donespec init --template python --yes
```

This tells any agent:

```text
The task is not done unless Python is available, Ruff passes, formatting is valid, and pytest passes.
```

For Node:

```bash
donespec init --template node --yes
```

This tells any agent:

```text
The task is not done unless package.json exists, npm test passes, and npm run build passes.
```

## Template examples

Example generated contracts live in:

```text
examples/templates/generic/done.json
examples/templates/python/done.json
examples/templates/node/done.json
examples/templates/docs/done.json
examples/templates/api/done.json
```

## Philosophy

Templates do not make DoneSpec less deterministic.

They make deterministic validation easier to adopt.

The contract remains:

```bash
donespec validate done.json
```
