# AGENTS.md

## Purpose

This repository uses DoneSpec as the deterministic completion gate for AI coding agent work.

DoneSpec exists because AI agents can produce plausible summaries without proving that the task is actually complete.

The rule is simple:

Done means deterministically verified.

## Non-negotiable completion rule

Before declaring any task complete, run:

donespec validate done.json

If the validation fails, the task is not complete.

Do not claim success.
Do not summarize the task as finished.
Do not ask the human to verify manually before attempting to fix the failing checks.

Instead:

1. Read the failing DoneSpec output.
2. Identify which check failed.
3. Fix the underlying issue.
4. Run DoneSpec again.
5. Repeat until validation passes.

## Agent workflow

When working in this repository:

1. Inspect the task requirements.
2. Inspect done.json.
3. Understand which checks define completion.
4. Make the smallest safe code/documentation changes required.
5. Run the relevant local commands.
6. Run:

donespec validate done.json

7. Only report completion if DoneSpec passes.

## If done.json exists

Treat done.json as the source of truth for task completion.

Do not weaken checks to make the task pass.
Do not remove failing checks unless the human explicitly requests a spec change.
Do not edit forbidden files listed under file_not_modified unless the task explicitly requires changing the validation contract.

## If done.json does not exist

Create a minimal task-specific done.json before claiming completion.

A good minimal DoneSpec should include at least one deterministic check, such as:

- a command check for tests, linting, formatting, or build
- a file_exists check for required generated files
- a regex_in_file check for required implementation markers
- a regex_absent check for forbidden patterns
- a file_not_modified check for protected files
- an http_check check for local service endpoints

## Forbidden behavior

Never say a task is done only because:

- code was edited
- tests were assumed to pass
- the implementation looks correct
- no error was visible
- the final answer sounds confident

A task is only done when DoneSpec passes.

## Final response requirements

When reporting completion, include:

- the DoneSpec command executed
- whether it passed
- the number of checks passed
- any important caveats

Example:

DoneSpec command executed:

donespec validate done.json

Result:

Validation passed. 9 checks passed.
Exit code: 0

## Compatibility

This file is intended for AI coding agents and coding assistants including Codex, Claude Code, Cursor, Windsurf, terminal agents, and any system capable of reading repository instructions and running shell commands.

The integration point is intentionally boring:

donespec validate done.json

No API key.
No model dependency.
No dashboard.
No hidden state.

Just deterministic validation.
