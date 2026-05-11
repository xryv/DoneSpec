# Agent Integration

DoneSpec is designed for any AI coding agent that can read files and run shell commands.

The integration model is intentionally small:

```bash
donespec validate done.json --strict
```

No API key.  
No model dependency.  
No orchestration layer.  
No dashboard.  
No hidden state.

DoneSpec stays outside the agent. The agent only needs to pass through the deterministic contract before claiming the task is complete.

## Core rule

An AI coding agent must not claim completion until DoneSpec passes.

Use this instruction with any coding agent:

```text
You may only claim completion after:

1. implementing the requested change
2. running the project's normal checks
3. running `donespec validate done.json --strict`
4. fixing any failures
5. reporting the final validation result

Do not weaken, remove, or bypass DoneSpec checks to make validation pass.
```

If DoneSpec fails, the task is not complete.

The agent should:

1. read the failing check
2. fix the underlying issue
3. run DoneSpec again
4. repeat until validation passes

## Codex

Codex-compatible workflows should use `AGENTS.md`.

Expected Codex workflow:

```text
read AGENTS.md
read done.json
modify code
run relevant project checks
run donespec validate done.json --strict
only report completion if validation passes
```

## Claude Code

Claude Code uses `CLAUDE.md`.

This repository keeps Claude-specific notes small and imports the shared protocol:

```text
@AGENTS.md
```

Expected Claude Code workflow:

```text
read CLAUDE.md
load AGENTS.md
inspect done.json
make changes
run project tests or checks
run donespec validate done.json --strict
report failures honestly
continue fixing until validation passes
```

## Cursor and VS Code

Cursor can use the same files and tasks as VS Code.

Recommended setup:

- keep `done.json` in the project root
- map `done.json` to `done.schema.json` for autocomplete
- run DoneSpec from the integrated terminal or a task
- instruct Cursor agents to validate before completion

The validation command is:

```bash
donespec validate done.json --strict
```

## Aider

Aider workflows should keep `done.json` visible and validate after edits.

Use this instruction:

```text
After changing files, run `donespec validate done.json --strict`.
If validation fails, inspect the failing check, fix the issue, and run validation again.
Do not accept conversational completion without validation.
```

## OpenAI Agents SDK

Use DoneSpec as an external command after file modifications.

The workflow does not need DoneSpec-specific runtime code:

```text
agent modifies files
agent runs project checks
agent runs donespec validate done.json --strict
agent reports success only on exit code 0
```

## Git hooks

This repository includes a pre-push hook:

```text
.githooks/pre-push
```

The hook runs DoneSpec before pushes. Install it with:

Windows PowerShell:

```powershell
.\scripts\install-git-hooks.ps1
```

Linux/macOS:

```bash
./scripts/install-git-hooks.sh
```

## CI enforcement

GitHub Actions and generic CI systems can run the same command agents run locally:

```yaml
- name: Validate DoneSpec contract strictly
  run: donespec validate done.json --strict
```

This creates repeatable validation layers:

```text
agent instructions
local terminal
pre-push hook
CI
```

## More examples

See [docs/integrations.md](integrations.md) for copy-paste examples for Codex, Claude Code, Cursor, Aider, OpenAI Agents SDK, GitHub Actions, and generic CI.
