# Installation

DoneSpec is a Python CLI package.

## With pipx

```bash
pipx install donespec
```

## With uv

```bash
uv tool install donespec
```

## From source

```bash
git clone https://github.com/donespec/donespec.git
cd donespec
python -m pip install -e ".[dev]"
```

## Verify

```bash
donespec --version
donespec validate done.json
```
