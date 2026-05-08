# DoneSpec

[![PyPI version](https://img.shields.io/pypi/v/donespec.svg)](https://pypi.org/project/donespec/)
[![Python versions](https://img.shields.io/pypi/pyversions/donespec.svg)](https://pypi.org/project/donespec/)
[![CI](https://github.com/xryv/DoneSpec/actions/workflows/ci.yml/badge.svg)](https://github.com/xryv/DoneSpec/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/xryv/DoneSpec.svg)](https://github.com/xryv/DoneSpec/blob/main/LICENSE)

> Done means deterministically verified.

DoneSpec is a tiny CLI for validating whether an AI coding agent actually completed a task.

It reads a machine-readable `done.json`, executes deterministic checks, and exits with `0` only when the task is verifiably complete.

```bash
pip install donespec
```

```bash
donespec validate done.json
```

```text
DoneSpec validation: fix-auth-bug

✓ npm tests passed  (1242.7ms)
✓ auth.ts exists  (0.2ms)
✓ returnTo is implemented  (0.5ms)
✗ shared types untouched  (12.1ms)
  Forbidden path modified: src/types.ts

Validation failed.
1 check failed.
Exit code: 1
```

## 1. Problem

AI coding agents are increasingly good at producing code, but they still frequently claim work is complete when it is not.

Common failures:

- tests were not run,
- tests fail,
- files were modified incorrectly,
- requirements were partially implemented,
- forbidden paths were touched,
- expected outputs were hallucinated,
- runtime invariants were broken.

Humans are left reading optimistic summaries instead of deterministic evidence.

DoneSpec gives every task a local, reproducible completion contract.

## 2. Why AI agents fail

AI agents optimize for plausible task completion. Software delivery requires verified task completion.

An agent can say:

> I fixed the auth bug and all tests pass.

DoneSpec asks:

- Did the configured command exit successfully?
- Does the expected file exist?
- Does the required implementation marker exist?
- Was a forbidden file modified?
- Does the HTTP endpoint return the expected status?

No vibes. No screenshots. No hidden judgement. Just deterministic checks.

## 3. What DoneSpec solves

DoneSpec introduces a small validation layer between AI coding agents and human trust.

It provides:

- a machine-readable `done.json`,
- deterministic local checks,
- CI/CD integration,
- structured JSON output,
- a checker registry for future extension,
- zero LLM dependency in the validation path.

DoneSpec is not an AI wrapper, chatbot, dashboard, or orchestration system.

It is developer infrastructure.

## 4. Installation

### pip

```bash
pip install donespec
```

### pipx

```bash
pipx install donespec
```

### uv

```bash
uv tool install donespec
```

### from source

```bash
git clone https://github.com/xryv/DoneSpec.git
cd DoneSpec
python -m pip install -e ".[dev]"
```

Verify:

```bash
donespec --version
```

### initialize a DoneSpec-ready project

```bash
donespec init --yes
donespec validate done.json
```

This creates a starter `done.json`, agent instructions, VS Code tasks, and optional Git hook files.

Read the full guide:

[docs/init.md

### Inspect project readiness

```bash
donespec doctor
```

Use `doctor` to check whether a repository has the expected DoneSpec files, agent instructions, editor tasks, hooks, and CI integration.

Machine-readable output:

```bash
donespec doctor --json
```

Read the full guide:

```text
docs/doctor.md
```

](docs/init.md)

## 5. Quick example

Create `done.json`:

```json
{
  "version": "1.0",
  "task_id": "fix-auth-bug",
  "must_pass": [
    {
      "type": "command",
      "name": "npm tests passed",
      "run": "npm test"
    },
    {
      "type": "file_exists",
      "name": "auth.ts exists",
      "path": "src/auth.ts"
    },
    {
      "type": "regex_in_file",
      "name": "returnTo is implemented",
      "path": "src/auth.ts",
      "pattern": "returnTo"
    }
  ],
  "must_not": [
    {
      "type": "file_not_modified",
      "name": "shared types untouched",
      "path": "src/types.ts"
    }
  ]
}
```

Run:

```bash
donespec validate done.json
```

Machine-readable output:

```bash
donespec validate done.json --json
```

## 6. CLI usage

```bash
donespec validate done.json
```

Options:

```text
--json       Emit machine-readable JSON output.
--root PATH  Project root. Defaults to the spec file directory.
--fail-fast  Stop after first failed check.
```

Exit codes:

| Code | Meaning |
| ---: | ------- |
| 0 | Validation passed |
| 1 | Validation failed |
| 2 | Invalid spec or runtime error |

## Supported checks

### `command`

Runs a shell command and validates the exit code.

```json
{
  "type": "command",
  "name": "tests pass",
  "run": "pytest",
  "expected_exit_code": 0,
  "timeout_seconds": 120
}
```

### `file_exists`

Checks that a file or directory exists.

```json
{
  "type": "file_exists",
  "path": "src/auth.ts"
}
```

### `regex_in_file`

Checks that a regex exists in a file.

```json
{
  "type": "regex_in_file",
  "path": "src/auth.ts",
  "pattern": "returnTo"
}
```

Optional flags:

```json
{
  "flags": ["IGNORECASE", "MULTILINE", "DOTALL"]
}
```

### `regex_absent`

Checks that a regex does not exist in a file.

```json
{
  "type": "regex_absent",
  "path": "src/auth.ts",
  "pattern": "console\\.log"
}
```

### `file_not_modified`

Checks Git status to ensure a file or path was not modified, staged, deleted, or newly added.

```json
{
  "type": "file_not_modified",
  "path": "src/types.ts"
}
```

### `http_check`

Makes an HTTP request and validates the response status.

```json
{
  "type": "http_check",
  "url": "http://127.0.0.1:8000/health",
  "method": "GET",
  "expected_status": 200,
  "timeout_seconds": 3
}
```

## 7. CI integration

### GitHub Actions

```yaml
name: DoneSpec

on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: xryv/DoneSpec@v0.2.0
        with:
          spec: done.json
          root: .
```

The action installs DoneSpec, runs validation, and fails CI if any check fails.

### Direct CI command

```yaml
- run: python -m pip install donespec
- run: donespec validate done.json
```

### Agent integrations

DoneSpec includes a practical multi-agent workflow for Codex, Claude Code, VS Code tasks, Git hooks, and CI enforcement.

Read the full guide:

[docs/agent-integration.md](docs/agent-integration.md)


## 8. Philosophy

DoneSpec is intentionally boring.

It should feel closer to ESLint, Prettier, pytest, or `package.json` scripts than to an AI platform.

Principles:

- local first,
- deterministic only,
- minimal dependencies,
- no accounts,
- no dashboard in the MVP,
- no LLM calls in validation,
- composable with any agent,
- simple enough for solo developers,
- strict enough for CI.

AI agents may generate work. DoneSpec verifies completion.

## 9. Roadmap

DoneSpec is designed for future extension, but the MVP stays small.

Planned directions:

- more deterministic checkers,
- generated `done.json` templates,
- MCP server integration,
- AI agent integrations,
- VSCode extension,
- cloud dashboard,
- analytics,
- multi-agent validation.

Not in the MVP:

- authentication,
- database,
- SaaS dashboard,
- orchestration system,
- LLM dependency.

## Repository layout

```text
.
├── action.yml
├── done.json
├── done.schema.json
├── docs/
├── examples/
├── pyproject.toml
├── src/
│   └── donespec/
│       ├── cli.py
│       ├── engine.py
│       ├── loader.py
│       ├── models.py
│       ├── output.py
│       ├── schema.py
│       └── checkers/
└── tests/
```

## Development

```bash
python -m pip install -e ".[dev]"
ruff check .
ruff format .
pytest
donespec validate done.json
```

## Release

DoneSpec `v0.2.0` is available on PyPI:

```bash
pip install donespec
```

GitHub release:

```text
https://github.com/xryv/DoneSpec/releases/tag/v0.2.0
```

PyPI package:

```text
https://pypi.org/project/donespec/
```

## License

MIT
