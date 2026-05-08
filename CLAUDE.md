@AGENTS.md

## Claude Code specific notes

This repository uses DoneSpec as the completion gate.

Before reporting a task as complete, run:

donespec validate done.json

If validation fails, continue fixing the task until DoneSpec passes.

Use concise implementation plans for code changes.
Prefer small, reviewable changes.
Do not weaken done.json checks to make validation pass unless the human explicitly asks to change the validation contract.
