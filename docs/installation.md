# Installation

DoneSpec is a Python CLI package.

## Standard install

```bash
python -m pip install donespec
```

Verify the installed CLI:

```bash
donespec --version
donespec --help
```

First validation command:

```bash
donespec validate done.json --strict
```

## Recommended virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install donespec
donespec --version
```

Linux/macOS:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install donespec
donespec --version
```

## Windows PATH troubleshooting

If PowerShell cannot find `donespec` after installing into a project virtual environment, put the venv scripts directory first in `PATH` for the current shell:

```powershell
$env:PATH = "$PWD\.venv\Scripts;$env:PATH"
donespec --version
```

If the package was installed with `pip --user`, make sure the Python user scripts directory is on `PATH`.

## Local development install

```bash
git clone https://github.com/xryv/DoneSpec.git
cd DoneSpec
python -m pip install -e ".[dev]"
```

Run the local verification set:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json --strict
```

## Local wheel install

Build the package:

```bash
python -m build
```

Install the wheel in a clean environment.

Windows PowerShell:

```powershell
python -m venv .venv-wheel-smoke
.\.venv-wheel-smoke\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .\dist\donespec-X.Y.Z-py3-none-any.whl
donespec --version
```

Linux/macOS:

```bash
python -m venv .venv-wheel-smoke
. .venv-wheel-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install ./dist/donespec-X.Y.Z-py3-none-any.whl
donespec --version
```

## PyPI smoke test

Use a clean environment so the test proves the published package installs on its own.

```bash
python -m venv .venv-pypi-smoke
. .venv-pypi-smoke/bin/activate
python -m pip install --upgrade pip
python -m pip install --no-cache-dir donespec
donespec --version
donespec --help
donespec init smoke --yes
donespec validate smoke/done.json --strict
```

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
```

## pipx and uv

For tool-style installs:

```bash
pipx install donespec
```

```bash
uv tool install donespec
```
