# DoneSpec v1.0 release runbook

## Purpose

This runbook describes the final human-executable procedure for releasing DoneSpec v1.0.

It does not mean v1.0 has already been released. It is an operational checklist for a maintainer to follow when the release is ready.

## Release principles

- No feature expansion during release.
- No weakening of DoneSpec checks to make a release pass.
- No publishing unless all gates pass.
- No hidden network calls.
- Local-first validation first.
- CI validation second.
- Package validation third.
- PyPI and GitHub release last.

The release must preserve the positioning:

```text
AI agents say tasks are done.
DoneSpec verifies they actually are.
```

DoneSpec is the deterministic completion layer for AI coding agents.

## Pre-release freeze

Before starting the release, freeze:

- runtime behavior
- schema semantics
- CLI command names
- check types
- documentation positioning
- package metadata
- release notes

Do not add features, change validation semantics, rename commands, add dependencies, or reframe DoneSpec as a platform during release.

## Required clean state

Start from the repository root on Windows PowerShell:

```powershell
cd C:\Users\cerqu\OneDrive\Desktop\Area_Desenvolvimento\DoneSpec
.\.venv\Scripts\Activate.ps1
$ErrorActionPreference = "Stop"
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
git status
```

The working tree must be clean before release work starts.

If `git status` shows unrelated local changes, stop and resolve them before continuing.

Linux/macOS equivalent:

```bash
cd /path/to/DoneSpec
. .venv/bin/activate
git status
```

## Local validation gate

Run:

```powershell
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

Both DoneSpec validations must pass. Do not weaken the `README untouched during validation` check or any other check to make release validation pass.

If any local validation command fails, stop the release and fix the underlying issue in a normal change before restarting the runbook.

## Package build gate

Build from a clean local state:

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
python -m build
python -m twine check dist/*
```

Expected artifacts:

```text
dist/donespec-1.0.0-py3-none-any.whl
dist/donespec-1.0.0.tar.gz
```

Linux/macOS equivalent:

```bash
rm -rf dist
python -m build
python -m twine check dist/*
```

## Local wheel smoke test

Test the built wheel from a clean environment.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv-wheel-smoke -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force wheel-smoke -ErrorAction SilentlyContinue
python -m venv .venv-wheel-smoke
.\.venv-wheel-smoke\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .\dist\donespec-1.0.0-py3-none-any.whl
donespec --version
donespec --help
donespec init wheel-smoke --yes
donespec validate .\wheel-smoke\done.json --strict
```

Linux/macOS equivalent:

```bash
rm -rf .venv-wheel-smoke wheel-smoke
python -m venv .venv-wheel-smoke
. .venv-wheel-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install ./dist/donespec-1.0.0-py3-none-any.whl
donespec --version
donespec --help
donespec init wheel-smoke --yes
donespec validate wheel-smoke/done.json --strict
```

Return to the repository virtual environment before continuing:

```powershell
deactivate
.\.venv\Scripts\Activate.ps1
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
```

## PyPI smoke test after publish

Run this only after v1.0.0 has been published to PyPI.

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force .venv-pypi-smoke -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force pypi-smoke -ErrorAction SilentlyContinue
python -m venv .venv-pypi-smoke
.\.venv-pypi-smoke\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-cache-dir --index-url https://pypi.org/simple donespec==1.0.0
donespec --version
donespec init pypi-smoke --yes
donespec validate .\pypi-smoke\done.json --strict
```

Linux/macOS equivalent:

```bash
rm -rf .venv-pypi-smoke pypi-smoke
python -m venv .venv-pypi-smoke
. .venv-pypi-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir --index-url https://pypi.org/simple donespec==1.0.0
donespec --version
donespec init pypi-smoke --yes
donespec validate pypi-smoke/done.json --strict
```

## GitHub Actions gate

All required GitHub Actions workflows must be green before tagging or publishing.

Verify:

- main CI
- cross-platform verification
- package verification workflow
- Windows jobs
- Linux jobs
- macOS jobs

The cross-platform workflow should validate linting, formatting, tests, normal DoneSpec validation, strict DoneSpec validation, JSON explain output, CLI smoke checks, and init smoke validation.

The package verification workflow must build the package, run `twine check`, install the local wheel, and validate a smoke project strictly.

## Version bump procedure

Do not perform this bump until the release decision is made.

For v1.0, expected files to inspect and update:

- `pyproject.toml`
- `src/donespec/__init__.py`
- `README.md`, if version references exist
- `docs/integrations.md`, if action version references exist
- `CHANGELOG.md`
- `docs/releases/v1.0.0-draft.md`, if needed

After the bump, rerun the local validation gate and package build gate.

## Tagging procedure

Documented commands only. Execute them only after all prior gates pass.

```powershell
git tag -a v1.0.0 -m "v1.0.0 - Deterministic completion validation for AI coding agents"
git push origin v1.0.0
```

Confirm the tag points to the intended release commit:

```powershell
git show --stat v1.0.0
```

## PyPI publication procedure

Documented command only. Execute it only after validation, build, wheel smoke test, CI, and tag checks pass.

```powershell
python -m twine upload dist/*
```

After upload, run the PyPI smoke test above.

## GitHub release procedure

Use `docs/releases/v1.0.0-draft.md` as the starting point for the GitHub Release body.

Launch copy drafts are available in `docs/launch/README.md`.

Before publishing the GitHub Release:

- confirm the release points to tag `v1.0.0`
- attach the wheel and sdist if desired
- preserve the deterministic completion validation positioning
- do not overclaim correctness
- do not claim DoneSpec replaces tests, CI, or human review

## Rollback / failure handling

If tests fail:

- stop the release
- fix the underlying issue in a normal commit
- restart from the local validation gate

If DoneSpec fails:

- read the failing check
- fix the underlying issue
- do not weaken, remove, or bypass checks
- rerun both normal and strict validation

If build fails:

- stop before tagging or publishing
- inspect package metadata and build configuration
- rebuild only after the issue is fixed

If `twine check` fails:

- do not upload to PyPI
- fix metadata or README rendering problems
- rebuild and rerun `python -m twine check dist/*`

If PyPI upload partially succeeds:

- do not re-upload the same version blindly
- inspect which artifacts were accepted
- treat PyPI as immutable for accepted files
- decide whether to continue with the accepted release or prepare a patch release

If GitHub Actions fail after tag:

- do not publish the GitHub Release until the failure is understood
- if the tag is wrong, create a corrective commit and a new tag according to project policy
- if the package was already published, document the failure and decide whether a patch release is required

## Final release declaration

DoneSpec v1.0 can only be declared released after:

- clean git state
- local validation passed
- strict DoneSpec passed
- package build passed
- local wheel smoke test passed
- GitHub Actions passed
- PyPI v1.0 install smoke test passed
- GitHub Release published

Every required v1.0.0 release item is now complete.
