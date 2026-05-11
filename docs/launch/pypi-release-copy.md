# PyPI release copy draft

DoneSpec is a tiny local-first CLI for deterministic completion validation.

AI agents say tasks are done.
DoneSpec verifies they actually are.

DoneSpec uses explicit `done.json` contracts and normal exit codes so AI coding agents, humans, git hooks, and CI can agree on whether a task passed its completion checks.

```bash
pip install donespec
donespec init --yes
donespec validate done.json
donespec validate done.json --strict
```

DoneSpec is the deterministic completion layer for AI coding agents.

It does not replace tests, CI, or human review. It does not call an LLM, run a cloud service, orchestrate agents, or validate semantic correctness. It validates explicit local contracts.
