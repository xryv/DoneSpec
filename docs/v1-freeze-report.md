# DoneSpec v1.0 freeze report

## Status

This is a pre-release readiness report.

This document does not publish DoneSpec v1.0. It does not create a tag, publish to PyPI, or create a GitHub Release.

No v1.0 release has been published by this document.

No v1.0 tag has been created by this document.

No PyPI publication has happened by this document.

## Product definition

```text
AI agents say tasks are done.
DoneSpec verifies they actually are.
```

```text
DoneSpec is the deterministic completion layer for AI coding agents.
```

## What DoneSpec is

- local-first CLI
- deterministic validation tool
- `done.json` contract checker
- CI-friendly completion gate
- composable infrastructure primitive
- agent-agnostic verification layer

## What DoneSpec is not

- not an orchestration platform
- not an AI framework
- not a SaaS
- not an agent runtime
- not a workflow engine
- not a memory layer
- not a replacement for tests
- not a replacement for human review

## Current validated surfaces

- CLI `validate` command for human and JSON output
- strict mode for stronger contract hygiene
- `explain` command for non-executing contract inspection
- `doctor` command for project readiness inspection
- `init` command for project bootstrap
- template discovery and starter contracts
- `add-check` contract authoring workflow
- JSON Schema export and packaged schema files
- GitHub Action metadata for DoneSpec validation
- VS Code and editor schema support documentation
- agent integration examples for Codex, Claude Code, Cursor, Aider, OpenAI Agents SDK, and GitHub Actions
- forbidden-file demo documentation and scripts
- package verification workflow for build, `twine check`, local wheel install, and smoke validation
- cross-platform workflow for Windows, Linux, and macOS
- release checklist and v1 release runbook
- v1 release candidate audit and v1 release notes draft
- OSS launch asset drafts

## Current validation gate

Before v1.0, run:

```powershell
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"

python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
python -m build
python -m twine check dist/*
```

The package verification workflow should also build the package, run `twine check`, install from the local wheel, and validate a smoke project strictly.

## Current DoneSpec check count

Verified locally before this report was written:

- `donespec validate done.json` passed with 326 checks.
- `donespec validate done.json --strict` passed with 326 checks.

## Known caveats

- Local Git commands still warn: `unable to access 'C:\Users\cerqu/.config/git/ignore': Permission denied`.
- v1.0 has not been tagged.
- v1.0 has not been published to PyPI.
- The PyPI smoke test must be repeated after final publication.
- GitHub Actions should be checked after this report is pushed.

## Release freeze recommendation

Recommendation: DoneSpec is ready to enter v1.0 release freeze if all local gates, package verification, and GitHub Actions checks are green.
