# Cross-platform verification

DoneSpec must behave predictably across Windows, Linux, and macOS.

This matters because DoneSpec is infrastructure for AI coding agents, local developer workflows, git hooks, and CI pipelines.

The goal is not platform-specific cleverness.

The goal is boring, deterministic portability.

```text
same done.json
same validation semantics
same exit codes
same trust contract
```

## Automated GitHub Actions matrix

DoneSpec includes an automated cross-platform GitHub Actions workflow:

```text
.github/workflows/cross-platform.yml
```

The workflow verifies DoneSpec on:

```text
ubuntu-latest
windows-latest
macos-latest
```

It runs:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
donespec explain done.json --strict --json
donespec templates
donespec doctor .
donespec init ci-smoke --yes
donespec validate ci-smoke/done.json --strict
```

This gives DoneSpec a real CI-backed portability gate before v1.0.

The goal is not to add platform complexity.

The goal is to prove the same small CLI behaves consistently everywhere.

## Required platforms

Before v1.0, verify DoneSpec on:

```text
Windows PowerShell
Linux shell
macOS shell
GitHub Actions Ubuntu runner
```

## Core verification matrix

Every platform should verify:

```bash
donespec --version
donespec --help
donespec init smoke-project --yes
donespec explain smoke-project/done.json
donespec explain smoke-project/done.json --json
donespec validate smoke-project/done.json
donespec validate smoke-project/done.json --strict
donespec doctor smoke-project
donespec templates
```

## Windows PowerShell smoke test

```powershell
cd C:\Users\cerqu\OneDrive\Desktop\Area_Desenvolvimento

Remove-Item -Recurse -Force DoneSpecSmokeWindows -ErrorAction SilentlyContinue
mkdir DoneSpecSmokeWindows
cd DoneSpecSmokeWindows

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install donespec

donespec --version
donespec --help

donespec init smoke-project --yes

donespec explain .\smoke-project\done.json
donespec explain .\smoke-project\done.json --json | python -m json.tool > $null

donespec validate .\smoke-project\done.json
donespec validate .\smoke-project\done.json --strict

donespec doctor .\smoke-project
donespec templates
```

Expected result:

```text
Validation passed.
Exit code: 0
```

## Linux smoke test

```bash
mkdir -p /tmp/donespec-smoke-linux
cd /tmp/donespec-smoke-linux

python -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install donespec

donespec --version
donespec --help

donespec init smoke-project --yes

donespec explain smoke-project/done.json
donespec explain smoke-project/done.json --json | python -m json.tool > /dev/null

donespec validate smoke-project/done.json
donespec validate smoke-project/done.json --strict

donespec doctor smoke-project
donespec templates
```

Expected result:

```text
Validation passed.
Exit code: 0
```

## macOS smoke test

```bash
mkdir -p /tmp/donespec-smoke-macos
cd /tmp/donespec-smoke-macos

python3 -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install donespec

donespec --version
donespec --help

donespec init smoke-project --yes

donespec explain smoke-project/done.json
donespec explain smoke-project/done.json --json | python -m json.tool > /dev/null

donespec validate smoke-project/done.json
donespec validate smoke-project/done.json --strict

donespec doctor smoke-project
donespec templates
```

Expected result:

```text
Validation passed.
Exit code: 0
```

## Local wheel smoke test

Before publishing a release, test the built wheel directly.

Windows PowerShell:

```powershell
cd C:\Users\cerqu\OneDrive\Desktop\Area_Desenvolvimento

Remove-Item -Recurse -Force DoneSpecWheelSmoke -ErrorAction SilentlyContinue
mkdir DoneSpecWheelSmoke
cd DoneSpecWheelSmoke

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install ..\DoneSpec\dist\donespec-X.Y.Z-py3-none-any.whl

donespec --version
donespec init wheel-smoke --yes
donespec validate .\wheel-smoke\done.json --strict
```

Linux/macOS:

```bash
mkdir -p /tmp/donespec-wheel-smoke
cd /tmp/donespec-wheel-smoke

python -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install /path/to/DoneSpec/dist/donespec-X.Y.Z-py3-none-any.whl

donespec --version
donespec init wheel-smoke --yes
donespec validate wheel-smoke/done.json --strict
```

## PyPI smoke test

After publishing:

```bash
python -m pip install --no-cache-dir --index-url https://pypi.org/simple donespec==X.Y.Z

donespec --version
donespec init pypi-smoke --yes
donespec validate pypi-smoke/done.json --strict
```

## GitHub Actions smoke test

A minimal CI verification should run:

```yaml
name: DoneSpec smoke test

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  smoke:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install DoneSpec
        run: pip install donespec

      - name: Verify CLI
        run: |
          donespec --version
          donespec --help

      - name: Validate contract
        run: donespec validate done.json --strict
```

## Encoding verification

DoneSpec output must not crash on Windows terminals with legacy encodings.

Verify:

```powershell
donespec explain done.json --strict | Out-Null
donespec validate done.json --strict
```

This protects against Unicode encoding failures in PowerShell and redirected output.

## Git hook verification

Windows PowerShell:

```powershell
.\scripts\install-git-hooks.ps1
git config core.hooksPath
```

Unix:

```bash
./scripts/install-git-hooks.sh
git config core.hooksPath
```

Expected result:

```text
.githooks
```

## Pass criteria

A platform passes verification when:

```text
✓ package installs cleanly
✓ CLI starts
✓ init succeeds
✓ explain succeeds
✓ explain --json emits valid JSON
✓ validate succeeds
✓ validate --strict succeeds
✓ doctor succeeds
✓ templates succeeds
✓ exit codes are stable
✓ no encoding crash occurs
```

## v1.0 rule

Do not declare DoneSpec v1.0 complete until the cross-platform matrix is verified.

DoneSpec should feel the same everywhere:

```text
local
deterministic
small
boring
trustworthy
```


## Line ending stability

Windows runners must not rewrite repository text files from LF to CRLF during validation.

The cross-platform workflow configures:

```bash
git config --global core.autocrlf false
git config --global core.eol lf
```

The repository also uses `.gitattributes` to keep text files stable across Windows, Linux, and macOS.

This protects `file_not_modified` checks from false failures caused by line-ending conversion.
