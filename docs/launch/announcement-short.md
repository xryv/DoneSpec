# Short announcement draft

AI agents say tasks are done.
DoneSpec verifies they actually are.

DoneSpec is the deterministic completion layer for AI coding agents: a tiny local-first CLI that validates explicit `done.json` completion contracts.

It does not replace tests or review. It gives agents, humans, and CI the same pass/fail contract before a task is called complete.

```bash
pip install donespec
donespec init --yes
donespec validate done.json --strict
```

No cloud. No LLM dependency. No orchestration layer. Just deterministic completion validation.
