# `donespec doctor`

`donespec doctor` inspects a project and reports whether it is DoneSpec-ready.

It is designed to answer one question:

```text
Is this repository ready to use DoneSpec as an AI-agent completion gate?
```

## Run

```bash
donespec doctor
```

Machine-readable output:

```bash
donespec doctor --json
```

## What it checks

`donespec doctor` verifies required and optional integration checks.

Required checks:

- DoneSpec installed
- `done.json` exists
- `done.json` is valid JSON

Optional integration checks:

- `AGENTS.md`
- `CLAUDE.md`
- `.vscode/tasks.json`
- `.githooks/pre-push`
- `scripts/install-git-hooks.ps1`
- `scripts/install-git-hooks.sh`
- `.github/workflows/ci.yml`
- CI self-validation command
- Git repository
- Git hooks path

## Exit codes

| Exit code | Meaning |
|---:|---|
| 0 | Required DoneSpec checks passed |
| 1 | Required DoneSpec checks failed |

Optional checks may fail without causing exit code `1`.

This is intentional.

A project can be minimally DoneSpec-ready even if optional integrations such as VS Code tasks, Git hooks, or CI are not yet configured.

## Human-readable output

Example:

```text
DoneSpec doctor

? DoneSpec installed required  version 0.1.1
? done.json exists required  ./done.json
? done.json is valid JSON required  valid
? AGENTS.md exists  AGENTS.md
? CLAUDE.md exists  CLAUDE.md
? VS Code tasks exist  .vscode/tasks.json
? Git pre-push hook exists  .githooks/pre-push
? GitHub Actions workflow exists  missing
? Git hooks path configured  not configured

Project has the required DoneSpec files.
Some optional integration checks are missing.
```

## JSON output

Use JSON output for automation:

```bash
donespec doctor --json
```

Example shape:

```json
{
  "root": "/path/to/project",
  "required_passed": true,
  "all_passed": false,
  "checks": [
    {
      "name": "done.json exists",
      "passed": true,
      "details": "/path/to/project/done.json",
      "required": true
    }
  ]
}
```

## Recommended workflow

For a new project:

```bash
pip install donespec
donespec init --yes
donespec doctor
donespec validate done.json
```

If doctor reports optional integrations missing, you can progressively add them.

## Install Git hooks

If the project has hook files but Git hooks are not configured, run:

On Windows:

```powershell
.\scripts\install-git-hooks.ps1
```

On Linux/macOS:

```bash
./scripts/install-git-hooks.sh
```

Then run:

```bash
donespec doctor
```

The hook path should report:

```text
Git hooks path configured  .githooks
```

## CI integration

If CI is missing, add a GitHub Actions workflow that runs:

```bash
donespec validate done.json
```

DoneSpec uses CI as the final remote enforcement layer.

## Philosophy

`donespec doctor` is not a validator for task completion.

That is the job of:

```bash
donespec validate done.json
```

`doctor` verifies the project setup.

`validate` verifies task completion.
