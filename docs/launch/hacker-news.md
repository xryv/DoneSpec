# Hacker News draft

Title:

```text
Show HN: DoneSpec - deterministic completion validation for AI coding agents
```

Post:

AI agents say tasks are done. DoneSpec verifies they actually are.

I built DoneSpec because AI coding agents can produce convincing completion summaries while the task is not actually complete: tests fail, files are missing, forbidden files changed, or docs were skipped.

DoneSpec is a tiny local-first CLI around a `done.json` contract. The contract lists deterministic checks, and `donespec validate done.json --strict` returns a normal pass/fail exit code that works in a terminal, git hook, or CI.

Example:

```bash
pip install donespec
donespec init --yes
donespec validate done.json --strict
```

What it deliberately does not do: orchestrate agents, call an LLM, run a service, manage state, replace tests, replace CI, or replace review. It validates explicit contracts, not semantic correctness.

The goal is boring infrastructure: a deterministic completion layer for AI coding agents.

Feedback is welcome, especially from people using Codex, Claude Code, Cursor, Aider, OpenAI Agents SDK workflows, or agent-generated PRs in CI.
