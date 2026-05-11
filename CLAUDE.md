@AGENTS.md

## Claude Code specific notes

This repository uses DoneSpec as the completion gate.

Before reporting a task as complete, run:

donespec validate done.json --strict

If validation fails, continue fixing the task until DoneSpec passes.

Claude Code should:

1. read the task contract in done.json
2. make the requested change
3. run the project's normal tests or checks
4. run `donespec validate done.json --strict`
5. report failures honestly and continue fixing until validation passes

Use concise implementation plans for code changes.
Prefer small, reviewable changes.
Do not weaken done.json checks to make validation pass unless the human explicitly asks to change the validation contract.
