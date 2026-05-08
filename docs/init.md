# `donespec init`

`donespec init` bootstraps a project with a deterministic completion contract for AI coding agents.

It creates the files needed to make a repository DoneSpec-ready:

```bash
donespec init
```

For non-interactive usage:

```bash
donespec init --yes
```

## What it creates

By default, `donespec init --yes` creates:

```text
done.json
AGENTS.md
CLAUDE.md
.vscode/tasks.json
.githooks/pre-push
scripts/install-git-hooks.ps1
scripts/install-git-hooks.sh
```

## Why it exists

Without `init`, every project has to manually create:

- a validation contract,
- agent instructions,
- editor tasks,
- Git hooks,
- hook installers.

With `init`, adoption becomes:

```bash
pip install donespec
donespec init --yes
donespec validate done.json
```

## Default behavior

The default command:

```bash
donespec init --yes
```

creates an agent-ready project for:

- Codex-compatible agents via `AGENTS.md`,
- Claude Code via `CLAUDE.md`,
- VS Code via `.vscode/tasks.json`,
- local Git enforcement via `.githooks/pre-push`,
- Windows hook installation via `scripts/install-git-hooks.ps1`,
- Linux/macOS hook installation via `scripts/install-git-hooks.sh`.

## Agent modes

Create all agent instruction files:

```bash
donespec init --yes --agent all
```

Create only Codex-compatible instructions:

```bash
donespec init --yes --agent codex
```

Create Claude Code instructions:

```bash
donespec init --yes --agent claude
```

Create no agent instruction files:

```bash
donespec init --yes --agent none
```

## VS Code tasks

By default, `init` creates:

```text
.vscode/tasks.json
```

To skip VS Code tasks:

```bash
donespec init --yes --no-vscode
```

## Git hooks

By default, `init` creates:

```text
.githooks/pre-push
scripts/install-git-hooks.ps1
scripts/install-git-hooks.sh
```

To skip Git hooks:

```bash
donespec init --yes --no-hooks
```

## Overwriting existing files

By default, existing files are not overwritten.

To overwrite DoneSpec-generated files:

```bash
donespec init --yes --force
```

Use `--force` carefully. It replaces existing DoneSpec files with generated defaults.

## Recommended first run

For most projects:

```bash
pip install donespec
donespec init --yes
donespec validate done.json
```

Then review `done.json` and customize the checks for the actual project.

## Install Git hooks

On Windows:

```powershell
.\scripts\install-git-hooks.ps1
```

On Linux/macOS:

```bash
./scripts/install-git-hooks.sh
```

After installing hooks, every `git push` runs:

```bash
donespec validate done.json
```

If validation fails, the push is blocked.

## Expected output

Example:

```text
DoneSpec project initialized.

Created:
✓ done.json
✓ AGENTS.md
✓ CLAUDE.md
✓ .vscode/tasks.json
✓ .githooks/pre-push
✓ scripts/install-git-hooks.ps1
✓ scripts/install-git-hooks.sh

Next steps:
1. Review done.json
2. Run: donespec validate done.json
3. Optional: install Git hooks
```

## Philosophy

`donespec init` does not make agents smarter.

It makes project completion harder to fake.

The contract remains:

```bash
donespec validate done.json
```
