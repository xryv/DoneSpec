# GitHub release copy draft

Title:

```text
DoneSpec v1.0.0
```

This is draft copy for a future GitHub Release. It does not mean v1.0.0 has been published.

## Summary

AI agents say tasks are done. DoneSpec verifies they actually are.

DoneSpec is the deterministic completion layer for AI coding agents: a tiny local-first CLI for validating explicit `done.json` completion contracts.

## Highlights

- Local `done.json` completion contracts
- Deterministic checks with stable exit codes
- Human and JSON output
- Strict mode for release and CI gates
- JSON Schema support for editor autocomplete
- GitHub Actions usage
- Cross-platform verification
- Package build and wheel smoke-test documentation

## Installation

```bash
pip install donespec
```

## Quickstart

```bash
donespec init --yes
donespec validate done.json
donespec validate done.json --strict
```

## Validation gates

Before release, DoneSpec should pass:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

The package verification workflow should also build the package, run `twine check`, install the local wheel, and validate a smoke project strictly.

## Non-goals

DoneSpec is not:

- an orchestration platform
- an AI framework
- a SaaS
- an agent runtime
- a workflow engine
- an LLM tool
- a replacement for tests, CI, or human review

DoneSpec validates explicit contracts, not semantic correctness.

## Upgrade notes

For v1.0, keep existing `done.json` contracts local, explicit, and deterministic. Use `donespec validate done.json --strict` for release gates and agent completion gates.

## Links

- README: `README.md`
- Schema docs: `docs/schema.md`
- Integration docs: `docs/integrations.md`
- Package smoke test: `docs/package-smoke-test.md`
- v1 release runbook: `docs/v1-release-runbook.md`
