# DoneSpec

**AI agents say tasks are done.**

**DoneSpec verifies they actually are.**

The deterministic completion layer for AI coding agents.

DoneSpec turns "done" into a local, repeatable, machine-checkable contract.

<p align="center">
  <img src="docs/assets/demo-terminal.svg" alt="DoneSpec terminal demo showing deterministic validation failure and success" width="860">
</p>

---

## The Problem

AI coding agents can claim completion while tests fail, required files are missing, forbidden paths changed, or documentation was skipped.

DoneSpec makes completion explicit: a task is not done until `done.json` passes.

```text
Done means deterministically verified.
```

---

## Demo

The core demo is a forbidden-file scenario:

1. An agent modifies a file protected by `done.json`.
2. `donespec validate done.json` fails.
3. The issue is fixed.
4. DoneSpec passes.

Run it locally:

```bash
./scripts/demo-forbidden-file.sh
```

Windows PowerShell:

```powershell
.\scripts\demo-forbidden-file.ps1
```

See:

- [docs/demo.md](docs/demo.md)
- [docs/demo-transcript.md](docs/demo-transcript.md)
- [docs/demo-recording.md](docs/demo-recording.md)

---

## Install

```bash
pip install donespec
```

Check the installed version:

```bash
donespec --version
```

PyPI:

```text
https://pypi.org/project/donespec/0.8.0/
```

GitHub release:

```text
https://github.com/xryv/DoneSpec/releases/tag/v0.8.0
```

---

## 60-second quickstart

Create a completion contract:

```bash
donespec init --yes
```

Validate it:

```bash
donespec validate done.json
```

Use strict mode for serious agent workflows:

```bash
donespec validate done.json --strict
```

Inspect the contract without executing checks:

```bash
donespec explain done.json
```

Add a check safely:

```bash
donespec add-check done.json --type file_exists --name "README exists" --path README.md
```

---

## Example `done.json`

```json
{
  "$schema": "done.schema.json",
  "version": "1.0",
  "task_id": "ship-safe-change",
  "must_pass": [
    {
      "type": "file_exists",
      "name": "README exists",
      "path": "README.md"
    },
    {
      "type": "command",
      "name": "tests pass",
      "run": "pytest -q"
    },
    {
      "type": "regex_in_file",
      "name": "README explains DoneSpec",
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

The contract is plain JSON. Agents, humans, hooks, and CI can all read the same definition of completion.

---

## Example CLI Output

Passing:

```text
DoneSpec validation: ship-safe-change

+ README exists  (0.4ms)
+ tests pass  (812.4ms)
+ README explains DoneSpec  (0.6ms)

Validation passed. 3 checks passed.
Exit code: 0
```

Failing:

```text
DoneSpec validation: ship-safe-change

+ README exists  (0.4ms)
x lockfile untouched  (31.5ms)
  Forbidden path modified: uv.lock

Validation failed.
1 check failed.
Exit code: 1
```

DoneSpec uses Unicode status symbols when the output stream supports them and ASCII fallback when it does not.

---

## GitHub Actions

Use DoneSpec as a completion gate in CI:

```yaml
name: DoneSpec

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  donespec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: xryv/DoneSpec@v0.8.0

      - name: Validate completion contract
        run: donespec validate done.json --strict
```

The same contract runs locally, in git hooks, in CI, and inside agent workflows.

---

## Why deterministic validation matters

DoneSpec validates explicit contracts, not confidence.

It does not replace tests, CI, or human review. It gives them a small deterministic interface:

```text
agent claim -> done.json -> deterministic checks -> exit code
```

That means:

- completion requirements are inspectable
- failures are machine-readable and repeatable
- CI can enforce the same contract agents see locally
- reviewers can inspect what "done" actually means

---

## AI Agent Integration

DoneSpec works with coding agents because it has no agent runtime, API key, SaaS service, memory layer, or LLM dependency.

A useful agent instruction is:

```text
Before claiming completion, run:

donespec validate done.json --strict

If validation fails, the task is not complete.
Do not weaken done.json to make validation pass unless explicitly requested by the human.
```

Useful with:

- Codex
- Claude Code
- Cursor
- Aider
- OpenAI Agents SDK
- GitHub Actions
- local shell workflows
- multi-agent coding workflows

See:

- [docs/integrations.md](docs/integrations.md)
- [docs/agent-integration.md](docs/agent-integration.md)

---

## Core Philosophy

DoneSpec stays small on purpose:

- local-first
- no cloud
- no LLM dependency
- no orchestration
- no database
- no hidden network calls
- deterministic exit codes

It is infrastructure, not a platform.

---

## Architecture Overview

```text
CLI
  reads done.json
  validates JSON Schema
  optionally applies strict contract hygiene
  runs deterministic checks
  emits human or JSON output
  exits 0, 1, or 2
```

The main pieces are:

- `donespec` CLI
- `done.json` completion contract
- deterministic checks
- packaged JSON Schema
- CI, git hooks, and agent instructions that call the same command

---

## Supported checks

| Check type          | Purpose                                      |
| ------------------- | -------------------------------------------- |
| `command`           | Run a shell command and verify the exit code |
| `file_exists`       | Require a file to exist                      |
| `regex_in_file`     | Require a pattern to exist in a file         |
| `regex_absent`      | Require a pattern to be absent from a file   |
| `file_not_modified` | Fail if a tracked file was modified          |
| `http_check`        | Check an HTTP endpoint response              |

DoneSpec is intentionally small. The goal is not to model every workflow; it is to provide a deterministic completion contract that composes with existing tools.

---

## Strict Mode

Strict mode validates contract hygiene before executing checks:

```bash
donespec validate done.json --strict
```

It catches:

- empty contracts
- unnamed checks
- duplicate check names
- duplicate check IDs
- invalid regex patterns
- absolute paths
- parent traversal paths

See [docs/strict.md](docs/strict.md).

---

## CLI Commands

`donespec explain done.json`

Explain a contract without executing it. Supports `--json`. See [docs/explain.md](docs/explain.md).

`donespec doctor`

Inspect whether a project is DoneSpec-ready. Supports `--json`. See [docs/doctor.md](docs/doctor.md).

`donespec schema`

Print or export the packaged JSON Schema. See [docs/schema.md](docs/schema.md).

`donespec templates`

List starter contract templates. See [docs/templates.md](docs/templates.md).

`donespec add-check`

Safely add a check and validate the updated contract before writing it. See [docs/authoring.md](docs/authoring.md).

`donespec init`

Create DoneSpec files in a project. See [docs/init.md](docs/init.md).

Editor support is documented in [docs/editor-support.md](docs/editor-support.md).

---

## Reliability And Field Notes

DoneSpec's own failures become permanent checks.

The first real Codex + VS Code pass found practical issues around release metadata, git hooks, line endings, and Windows output encoding. Those failures were turned into tests and DoneSpec checks.

See [docs/field-notes/first-codex-vscode-experience.md](docs/field-notes/first-codex-vscode-experience.md).

Cross-platform verification is documented in [docs/cross-platform-verification.md](docs/cross-platform-verification.md).

---

## v1.0 Readiness

DoneSpec v1.0 is a stabilization milestone, not a platform expansion.

See:

- [docs/v1-readiness.md](docs/v1-readiness.md)
- [docs/oss-launch.md](docs/oss-launch.md)
- [docs/release-checklist.md](docs/release-checklist.md)

---

## Roadmap to v1.0

The core is already capable. The path to v1.0 is stabilization:

- README polish
- CLI wording refinement
- schema freeze
- documentation hardening
- cross-platform verification
- release checklist
- changelog
- final GitHub and PyPI release
- OSS launch assets

DoneSpec should remain tiny, local-first, deterministic, composable, and infrastructure-focused.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Before opening a change, run:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

Contributions should protect the minimal core: determinism, clear CLI behavior, stable schema, cross-platform behavior, and documentation quality.

Avoid changes that turn DoneSpec into an orchestration platform, AI framework, SaaS service, agent runtime, workflow engine, plugin marketplace, or memory layer.
