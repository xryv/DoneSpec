# DoneSpec v1.0.0 release completion

DoneSpec v1.0.0 has been released.

This document records the final public release state after the v1 stabilization phase.

## Final product position

DoneSpec is:

```text
The deterministic completion layer for AI coding agents.
```

It remains:

* tiny
* local-first
* deterministic
* composable
* infrastructure-focused
* CI-friendly
* independent of LLM providers

DoneSpec is not:

* an orchestration platform
* an AI framework
* a SaaS product
* an agent runtime
* a workflow engine
* a memory system
* a dashboard

## Public release state

The v1.0.0 release is complete when all of the following are true:

```text
GitHub tag v1.0.0 exists
GitHub Release v1.0.0 exists
PyPI package donespec 1.0.0 exists
pip install donespec==1.0.0 works
README references the current v1.0.0 release
GitHub Actions are green
DoneSpec self-validation passes
DoneSpec strict self-validation passes
```

## Final validation gate

The release remains valid only if these commands pass:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

## Final statement

AI agents say tasks are done.

DoneSpec verifies they actually are.

DoneSpec v1.0.0 turns that principle into a public, installable, deterministic developer tool.
