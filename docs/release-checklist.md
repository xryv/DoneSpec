# Release checklist

This checklist keeps DoneSpec releases small, deterministic, repeatable, and trustworthy.

DoneSpec is not an AI framework, platform, orchestration layer, workflow engine, SaaS product, dashboard, database-backed system, or agent runtime.

DoneSpec is a tiny, local-first completion validator.

## Release principle

Every release must preserve the core identity:

```text
Done means deterministically verified.
```

A release is acceptable only when it improves determinism, stability, documentation, onboarding, CLI clarity, schema quality, test coverage, cross-platform reliability, packaging, or ecosystem integration.

A release is not acceptable if it expands DoneSpec into a platform.

## Pre-release validation

Confirm the working tree is clean:

```bash
git status
```

Use the repository virtual environment when running local checks.

Windows PowerShell:

```powershell
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
```

Run the required checks:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

Confirm CLI version and inspect the contract:

```bash
donespec --version
donespec explain done.json --strict
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

For v1.0, only release when the CLI, schema, docs, packaging, and onboarding experience feel stable.

## Build package

Remove old build artifacts:

```bash
rm -rf dist
```

Windows PowerShell:

```powershell
Remove-Item -Recurse -Force dist -ErrorAction SilentlyContinue
```

Build the package:

```bash
python -m build
```

Expected artifacts:

```text
dist/donespec-X.Y.Z-py3-none-any.whl
dist/donespec-X.Y.Z.tar.gz
```

## Twine check

Validate package metadata before upload:

```bash
python -m twine check dist/*
```

## Local wheel smoke test

Test the built wheel in a clean environment.

Windows PowerShell:

```powershell
python -m venv .venv-wheel-smoke
.\.venv-wheel-smoke\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .\dist\donespec-X.Y.Z-py3-none-any.whl
donespec --version
donespec --help
donespec init smoke --yes
donespec validate .\smoke\done.json --strict
donespec explain .\smoke\done.json --json
```

Linux/macOS:

```bash
python -m venv .venv-wheel-smoke
. .venv-wheel-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install ./dist/donespec-X.Y.Z-py3-none-any.whl
donespec --version
donespec --help
donespec init smoke --yes
donespec validate smoke/done.json --strict
donespec explain smoke/done.json --json
```

## PyPI upload

Upload manually after validation:

```bash
python -m twine upload dist/*
```

Do not automate publishing in repository code.

## PyPI smoke test

Verify the published package from a clean environment:

```bash
python -m venv .venv-pypi-smoke
. .venv-pypi-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir --index-url https://pypi.org/simple donespec==X.Y.Z
donespec --version
donespec --help
donespec init pypi-smoke --yes
donespec validate pypi-smoke/done.json --strict
```

Windows PowerShell:

```powershell
python -m venv .venv-pypi-smoke
.\.venv-pypi-smoke\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-cache-dir --index-url https://pypi.org/simple donespec==X.Y.Z
donespec --version
donespec --help
donespec init pypi-smoke --yes
donespec validate .\pypi-smoke\done.json --strict
```

## Git tag

Create and push an annotated tag:

```bash
git tag -a vX.Y.Z -m "vX.Y.Z - Release title"
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
Title: DoneSpec vX.Y.Z - Release title
```

The release description should include:

- summary
- what changed
- why it matters
- install command
- upgrade command
- validation command
- compatibility notes
- checklist confirmation

## Post-release validation

After publishing, verify from a clean environment:

```bash
pip install --no-cache-dir donespec==X.Y.Z
donespec --version
donespec init final-smoke --yes
donespec validate final-smoke/done.json --strict
```

Confirm the public metadata:

```text
PyPI page renders README correctly
GitHub release links to the tag
GitHub repository description is concise
GitHub topics match the project scope
```

## GitHub repository metadata

Suggested repository description:

```text
Deterministic completion validation for AI coding agents.
```

Suggested topics:

```text
ai-agents
developer-tools
cli
ci
validation
testing
json-schema
local-first
```

## v1.0 readiness gate

Do not declare v1.0 complete until these are true:

```text
README is polished
quickstart is clear
CLI output is stable
schema is stable
docs are complete
changelog exists
release checklist exists
examples are realistic
GitHub Action works
PyPI package installs cleanly
local wheel smoke test passes
Windows smoke test passes
Linux smoke test passes
macOS smoke test passes
no LLM dependencies exist
no platform expansion has happened
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

DoneSpec should feel boring in the best possible way: reliable, deterministic, local, composable, small, and standard-ready.
