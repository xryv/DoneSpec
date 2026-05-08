# Agent Integration

DoneSpec is designed to work with any AI coding agent that can read files and run shell commands.

The integration model is intentionally simple:

```bash
donespec validate done.json
```

No API key.  
No model dependency.  
No orchestration layer.  
No dashboard.  
No hidden state.

DoneSpec acts as a deterministic completion gate.

## Core rule

An AI coding agent must not claim a task is complete until DoneSpec passes.

```bash
donespec validate done.json
```

If DoneSpec fails, the task is not complete.

The agent should:

1. Read the failing check.
2. Fix the underlying issue.
3. Run DoneSpec again.
4. Repeat until validation passes.

## Codex

Codex-compatible workflows should use `AGENTS.md`.

This repository includes:

```text
AGENTS.md
```

The file instructs agents to treat `done.json` as the source of truth for task completion.

Expected Codex workflow:

```text
read AGENTS.md
read done.json
modify code
run relevant commands
run donespec validate done.json
only report completion if validation passes
```

## Claude Code

Claude Code uses `CLAUDE.md`.

This repository includes:

```text
CLAUDE.md
```

The file imports the shared agent protocol:

```text
@AGENTS.md
```

This avoids duplicating rules across agent-specific instruction files.

Expected Claude Code workflow:

```text
read CLAUDE.md
load AGENTS.md
inspect done.json
make changes
run donespec validate done.json
continue fixing until validation passes
```

## VS Code

This repository includes VS Code tasks:

```text
.vscode/tasks.json
```

Available tasks:

- DoneSpec: Validate
- DoneSpec: Validate JSON
- DoneSpec: Test
- DoneSpec: Lint
- DoneSpec: Format Check

In VS Code:

```text
Terminal → Run Task → DoneSpec: Validate
```

The default validation task runs:

```bash
donespec validate done.json
```

## Git hooks

This repository includes a pre-push hook:

```text
.githooks/pre-push
```

The hook runs:

```bash
donespec validate done.json
```

This prevents pushing code if DoneSpec fails locally.

### Install hooks on Windows

```powershell
.\scripts\install-git-hooks.ps1
```

### Install hooks on Linux/macOS

```bash
./scripts/install-git-hooks.sh
```

After installation, Git uses:

```text
core.hooksPath = .githooks
```

## CI enforcement

GitHub Actions also runs DoneSpec:

```yaml
- name: DoneSpec self-validation
  run: donespec validate done.json
```

This creates four validation layers:

```text
agent instructions
↓
VS Code task
↓
local pre-push hook
↓
GitHub Actions
```

## Recommended agent prompt

Use this instruction with any coding agent:

```text
This repository uses DoneSpec.

Before declaring the task complete, run:

donespec validate done.json

If validation fails, inspect the failing checks, fix the issue, and run DoneSpec again.

Do not claim completion until DoneSpec passes.
```

## Why this works

DoneSpec is agent-agnostic because it does not depend on any specific model, vendor, editor, or runtime.

Any system capable of running shell commands can use DoneSpec.

Compatible workflows include:

- Codex
- Claude Code
- Cursor
- Windsurf
- terminal agents
- local scripts
- CI/CD pipelines
- custom internal agents

The contract stays the same:

```bash
donespec validate done.json
```
