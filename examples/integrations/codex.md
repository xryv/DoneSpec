# Codex Integration Example

Paste this into `AGENTS.md` or a Codex task prompt:

```text
Before claiming the task is complete, run:

donespec validate done.json --strict

If validation fails, fix the issue and run it again.
Do not mark the task complete until DoneSpec passes.
Do not weaken, remove, or bypass DoneSpec checks to make validation pass.
```

DoneSpec does not replace tests, review, or engineering judgement. It is the deterministic completion gate.
