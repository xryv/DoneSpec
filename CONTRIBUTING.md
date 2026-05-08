# Contributing to DoneSpec

Thank you for considering a contribution to DoneSpec.

DoneSpec is intentionally small.

The goal is not to become an AI platform.

The goal is to remain a deterministic completion layer for AI coding agents.

```text
AI agents say tasks are done.

DoneSpec verifies they actually are.
```

## Core principle

DoneSpec exists to make completion explicit, local, inspectable, and deterministic.

Before contributing, keep this rule in mind:

```text
Done means deterministically verified.
```

## What belongs in DoneSpec

Good contributions usually improve:

- deterministic validation
- CLI clarity
- error messages
- schema quality
- documentation
- examples
- tests
- cross-platform behavior
- packaging
- release reliability
- integration guidance

## What does not belong in DoneSpec

Please avoid contributions that turn DoneSpec into:

- an AI agent framework
- an orchestration platform
- a hosted service
- a dashboard
- a workflow engine
- a database-backed system
- an agent memory layer
- a plugin marketplace
- an LLM-dependent tool

DoneSpec should remain boring infrastructure.

Small.

Local.

Composable.

Deterministic.

## Development setup

Clone the repository:

```bash
git clone https://github.com/xryv/DoneSpec.git
cd DoneSpec
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Unix/macOS:

```bash
. .venv/bin/activate
```

Install development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Validation before submitting

Before opening a pull request, run:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

The strict DoneSpec gate is required:

```bash
donespec validate done.json --strict
```

If validation fails, the task is not complete.

Do not weaken `done.json` to make a contribution pass unless the change explicitly updates the project contract for a valid reason.

## Pull request expectations

A good pull request should:

- explain the problem
- keep the change small
- include tests when behavior changes
- update documentation when user-facing behavior changes
- preserve deterministic behavior
- avoid hidden network calls
- avoid new AI/LLM dependencies
- pass strict DoneSpec validation

## Documentation contributions

Documentation changes are welcome when they make DoneSpec easier to understand.

Prefer:

- direct examples
- short commands
- clear failure cases
- clear success cases
- explicit completion contracts

Avoid:

- hype
- vague claims
- platform language
- promises that DoneSpec cannot guarantee

## Design philosophy

DoneSpec should feel like a missing infrastructure primitive.

Not a startup platform.

Not a framework.

Not magic.

Just a clear local contract and deterministic checks.
