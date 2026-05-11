# DoneSpec v1.0 release audit

This document audits DoneSpec as a v1.0 release.

It does not declare v1.0 released. It defines the gates that must pass before DoneSpec should proceed to a v1.0 release.

## Product definition

DoneSpec is a tiny local-first CLI for deterministic completion validation.

Its contract is `done.json`. Its job is to run explicit checks and return stable exit codes that humans, CI, hooks, and AI coding agents can all use.

Primary positioning:

```text
AI agents say tasks are done.
DoneSpec verifies they actually are.
```

DoneSpec is the deterministic completion layer for AI coding agents.

## Non-goals

DoneSpec must not expand into:

- an orchestration platform
- an AI framework
- a SaaS product
- an agent runtime
- a dashboard
- a database-backed system
- a memory layer
- a plugin marketplace
- an LLM-dependent tool
- a workflow engine

DoneSpec does not replace tests, CI, code review, security review, or engineering judgement.

## v1.0 readiness summary

DoneSpec is v1.0-ready only if it remains small, deterministic, local-first, composable, CI-friendly, and standard-ready.

The release has the expected shape for v1.0:

- a concise CLI
- an explicit `done.json` contract
- deterministic check execution
- strict mode for contract hygiene
- JSON output for automation
- schema documentation and editor guidance
- agent and CI integration examples
- release, installation, package smoke-test, and cross-platform verification docs

## Validation gates

Before v1.0 release, the release must pass:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
python -m build
python -m twine check dist/*
```

DoneSpec self-validation must be treated as a release gate, not a best-effort check.

## Installation gates

The release must verify these installation paths:

- standard `python -m pip install donespec`
- project virtual environment install
- local development install with `python -m pip install -e ".[dev]"`
- local wheel install from `dist/donespec-X.Y.Z-py3-none-any.whl`
- PyPI install from a clean environment after publishing

Each smoke test should verify:

```bash
donespec --version
donespec --help
donespec init smoke --yes
donespec validate smoke/done.json --strict
donespec explain smoke/done.json --json
```

Windows PowerShell smoke tests must also account for `.venv\Scripts` on `PATH`.

## Cross-platform gates

The release must remain portable across:

- Windows PowerShell
- Linux shell
- macOS shell
- GitHub Actions Ubuntu runners
- GitHub Actions Windows runners
- GitHub Actions macOS runners

The cross-platform workflow must verify linting, formatting, tests, normal validation, strict validation, JSON explain output, template listing, doctor output, and init smoke validation.

Windows output must remain safe for legacy encodings such as cp1252.

## Documentation gates

The documentation set must make DoneSpec understandable without product framing or platform language.

Required documentation gates:

- README explains the value quickly
- quickstart works in under a minute
- schema documentation defines `done.json` as a stable v1 contract format
- CLI UX documentation defines output and automation principles
- installation documentation covers pip, venv, local wheel, PyPI smoke tests, and Windows PATH guidance
- release checklist covers validation, build, twine check, wheel smoke test, PyPI smoke test, tags, GitHub release, and post-release validation
- package smoke-test documentation exists
- cross-platform verification documentation exists
- OSS launch guidance rejects platform framing

## Agent integration gates

Agent integration must stay boring.

DoneSpec does not need to run inside Codex, Claude Code, Cursor, Aider, OpenAI Agents SDK, or any other agent.

The required integration pattern is:

```bash
donespec validate done.json --strict
```

Agent documentation must continue to say:

- run project checks
- run DoneSpec strict validation
- fix failures before claiming completion
- do not weaken, remove, or bypass DoneSpec checks to make validation pass

## Security and trust boundaries

DoneSpec is local-first infrastructure.

Trust boundaries for v1.0:

- no hidden network calls
- no cloud control plane
- no credentials required
- no agent memory
- no LLM dependency
- no background service
- no database

DoneSpec validates explicit contracts. It does not infer intent, guarantee correctness, or certify code safety.

## Release blockers

Known release blockers before v1.0:

- any failing required validation gate
- broken package build or `twine check`
- failed local wheel smoke test
- failed PyPI smoke test after publish
- failed cross-platform workflow
- broken README, schema, installation, release, or integration links
- any new runtime dependency on LLMs, cloud services, databases, dashboards, or orchestration systems
- unclear CLI output or unstable exit code behavior
- package metadata that points to the wrong repository or misstates the project scope

At the time this audit document is prepared, no blocker should be considered cleared until the listed gates are run for the exact release commit.

## Final release conclusion

DoneSpec is ready to proceed toward v1.0 only if every validation, installation, cross-platform, documentation, agent integration, and packaging gate listed in this audit passes for the release commit.

Passing these gates means DoneSpec is ready to move forward in the release process. It does not mean v1.0 has already been released.
