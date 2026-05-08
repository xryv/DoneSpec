# Release instructions

## Preflight

```bash
ruff check .
ruff format --check .
pytest
```

## Version bump

Update:

- `pyproject.toml`
- `src/donespec/__init__.py`

## Build

```bash
python -m pip install --upgrade build twine
python -m build
python -m twine check dist/*
```

## Publish to PyPI

```bash
python -m twine upload dist/*
```

## Tag

```bash
git tag v0.1.0
git push origin v0.1.0
```

## GitHub Action release

For the action, publish a release tag such as `v1` after the CLI is available on PyPI.

Consumer usage:

```yaml
- uses: donespec/action@v1
  with:
    spec: done.json
```
