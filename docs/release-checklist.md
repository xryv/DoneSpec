# Release checklist

This checklist exists to keep DoneSpec releases small, deterministic, repeatable, and trustworthy.

DoneSpec is not an AI framework, platform, orchestration layer, workflow engine, SaaS product, dashboard, database-backed system, or agent runtime.

DoneSpec is a tiny, local-first completion validator.

## Release principle

Every release must preserve the core identity:

```text
Done means deterministically verified.
```

A release is acceptable only when it improves:

- determinism
- stability
- documentation
- onboarding
- CLI clarity
- schema quality
- test coverage
- cross-platform reliability
- ecosystem integration

A release is not acceptable if it expands DoneSpec into a platform.

## Before release

Confirm the working tree is clean:

```bash
git status
```

Run formatting and linting:

```bash
python -m ruff check .
python -m ruff format --check .
```

Run tests:

```bash
python -m pytest -q
```

Run DoneSpec self-validation:

```bash
donespec validate done.json
donespec validate done.json --strict
```

Confirm CLI version:

```bash
donespec --version
```

Inspect the contract:

```bash
donespec explain done.json --strict
```

Validate package metadata:

```bash
python -m twine check dist/*
```

## Version bump

Update the version in:

```text
pyproject.toml
src/donespec/__init__.py
README.md
```

Use semantic versioning:

```text
MAJOR.MINOR.PATCH
```

Guidance:

```text
PATCH: bug fixes, wording fixes, packaging fixes
MINOR: small compatible CLI improvements
MAJOR: stable public contract milestone
```

For v1.0, only release when the CLI, schema, docs, and onboarding experience feel stable.

## Build

Remove old build artifacts:

```bash
rm -rf dist
```

Build the package:

```bash
python -m build
```

Check distributions:

```bash
python -m twine check dist/*
```

Expected artifacts:

```text
dist/donespec-X.Y.Z-py3-none-any.whl
dist/donespec-X.Y.Z.tar.gz
```

## Local wheel smoke test

Create a clean environment and install the wheel:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install ../DoneSpec/dist/donespec-X.Y.Z-py3-none-any.whl
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install ..\DoneSpec\dist\donespec-X.Y.Z-py3-none-any.whl
```

Smoke test:

```bash
donespec --version
donespec --help
donespec init smoke-project --yes
donespec validate smoke-project/done.json
donespec validate smoke-project/done.json --strict
donespec explain smoke-project/done.json
```

## PyPI release

Upload:

```bash
python -m twine upload dist/*
```

Verify availability:

```bash
python -m pip cache purge
python -m pip --no-cache-dir index versions donespec
```

Install from PyPI in a clean environment:

```bash
python -m pip install --no-cache-dir --index-url https://pypi.org/simple donespec==X.Y.Z
```

Smoke test the PyPI package:

```bash
donespec --version
donespec --help
donespec init pypi-smoke --yes
donespec validate pypi-smoke/done.json --strict
```

## Git tag

Create an annotated tag:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z - Release title"
```

Push the tag:

```bash
git push origin vX.Y.Z
```

Confirm tags:

```bash
git tag
```

## GitHub release

Create a GitHub release with:

```text
Tag: vX.Y.Z
Title: DoneSpec vX.Y.Z — Release title
```

The release description should include:

- summary
- what changed
- why it matters
- install command
- upgrade command
- validation command
- compatibility notes
- full checklist confirmation

## Final release validation

After publishing, verify from a clean environment:

```bash
pip install --no-cache-dir donespec==X.Y.Z
donespec --version
donespec init final-smoke --yes
donespec validate final-smoke/done.json --strict
```

## v1.0 readiness gate

Do not declare v1.0 complete until these are true:

```text
✓ README is polished
✓ quickstart is clear
✓ CLI output is stable
✓ schema is stable
✓ docs are complete
✓ changelog exists
✓ release checklist exists
✓ examples are realistic
✓ GitHub Action works
✓ PyPI package installs cleanly
✓ Windows smoke test passes
✓ Linux smoke test passes
✓ macOS smoke test passes
✓ no LLM dependencies exist
✓ no platform expansion has happened
```

## Anti-expansion checklist

Before every release, confirm DoneSpec did not become:

```text
x orchestration platform
x AI framework
x SaaS service
x agent runtime
x workflow engine
x dashboard
x database-backed system
x plugin marketplace
x memory layer
x LLM-dependent tool
```

## Release philosophy

DoneSpec should feel boring in the best possible way.

Reliable.

Deterministic.

Local.

Composable.

Small.

Standard-ready.
