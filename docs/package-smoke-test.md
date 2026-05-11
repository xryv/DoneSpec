# Package smoke test

Use this checklist to prove the package installs and starts from a clean environment.

## Local wheel

Build the package first:

```bash
python -m build
```

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

## PyPI

Windows PowerShell:

```powershell
python -m venv .venv-pypi-smoke
.\.venv-pypi-smoke\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --no-cache-dir donespec
donespec --version
donespec --help
donespec init smoke --yes
donespec validate .\smoke\done.json --strict
donespec explain .\smoke\done.json --json
```

Linux/macOS:

```bash
python -m venv .venv-pypi-smoke
. .venv-pypi-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir donespec
donespec --version
donespec --help
donespec init smoke --yes
donespec validate smoke/done.json --strict
donespec explain smoke/done.json --json
```

## Automated package verification

Package verification also runs in GitHub Actions:

```text
.github/workflows/package-verification.yml
```

The workflow builds the package, runs `twine check`, installs from the local wheel, and validates a smoke project strictly.

It does not publish to PyPI.

## Pass criteria

The smoke test passes when:

```text
donespec --version exits 0
donespec --help exits 0
donespec init smoke --yes creates a contract
donespec validate smoke/done.json --strict exits 0
donespec explain smoke/done.json --json emits JSON
```
