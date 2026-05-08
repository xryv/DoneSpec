# DoneSpec v1.0 readiness

DoneSpec v1.0 should not feel like a larger product.

It should feel like a small infrastructure primitive that became obvious.

```text
AI agents say tasks are done.

DoneSpec verifies they actually are.
```

## DoneSpec v1.0 readiness gate

DoneSpec is ready for v1.0 only when the project feels:

- stable
- deterministic
- boring in the best possible way
- easy to install
- easy to explain
- easy to integrate
- safe to run locally
- credible as developer infrastructure
- small enough to understand quickly
- strict enough to trust

## Core identity

DoneSpec is:

```text
the deterministic completion layer for AI coding agents
```

DoneSpec is not:

- an orchestration platform
- an AI framework
- a SaaS product
- an agent runtime
- a workflow engine
- a dashboard
- a database-backed system
- a memory layer
- a plugin marketplace
- an LLM-dependent tool

## No platform expansion

No platform expansion should happen before v1.0.

Allowed work:

- README polish
- CLI wording refinement
- schema documentation
- test hardening
- cross-platform verification
- release notes
- demo assets
- installation polish
- integration examples
- PyPI metadata polish
- GitHub release polish

Disallowed work:

- databases
- authentication
- hosted services
- dashboards
- cloud control planes
- orchestration logic
- agent memory
- LLM integrations
- plugin systems
- background workers
- workflow engines

## v1.0 technical checklist

Before v1.0:

```text
? README explains value in under 10 seconds
? install flow works with pip install donespec
? quickstart works in under 60 seconds
? donespec init creates useful defaults
? donespec validate done.json works locally
? donespec validate done.json --strict works locally
? JSON output remains machine-readable
? schema export works
? schema docs are clear
? examples are realistic
? GitHub Action works
? git hooks work
? Windows smoke test passes
? Linux smoke test passes
? macOS smoke test passes
? PyPI install smoke test passes
? local wheel smoke test passes
? release checklist exists
? changelog is current
? docs are concise
? no LLM dependency exists
? no platform expansion exists
```

## v1.0 positioning checklist

The public message should be consistent:

```text
AI agents say tasks are done.
DoneSpec verifies they actually are.
```

Supporting phrases:

- deterministic completion validation
- local-first completion contracts
- CI-friendly trust layer
- done.json as an explicit completion contract
- pass/fail validation for agent work
- no AI magic
- no cloud dependency
- no runtime dependency

Avoid positioning DoneSpec as:

- an AI agent platform
- a workflow automation suite
- an AI coding framework
- a task manager
- a project management tool
- a hosted validation service

## Schema stability

Treat `done.json` as a future infrastructure primitive.

Before v1.0:

- avoid unnecessary field churn
- keep check semantics clear
- keep version handling predictable
- document supported fields
- keep strict mode conservative
- prefer explicit validation errors
- preserve backward compatibility where possible

## CLI stability

The CLI should feel sharp and minimal.

Expected commands:

```bash
donespec --version
donespec init --yes
donespec validate done.json
donespec validate done.json --strict
donespec explain done.json
donespec explain done.json --json
donespec schema --write done.schema.json
donespec doctor
donespec templates
donespec add-check done.json --type file_exists --name "README exists" --path README.md
```

The CLI should avoid:

- noisy output
- vague errors
- surprising side effects
- hidden network calls
- AI-specific assumptions
- platform-specific behavior

## Release confidence

A v1.0 release candidate should pass:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
python -m build
python -m twine check dist/*
```

Then verify installation from:

- local wheel
- PyPI
- clean Windows environment
- clean Linux environment
- clean macOS environment where possible

## Final rule

If a proposed change makes DoneSpec harder to explain, harder to install, harder to trust, or larger than necessary, it should not be part of v1.0.

The standard succeeds by staying small.
