# Contributing

DoneSpec is OSS-first infrastructure. Keep it boring, deterministic, and useful.

## Local setup

```bash
python -m pip install -e ".[dev]"
```

## Quality gate

```bash
ruff check .
ruff format --check .
pytest
```

## Adding a checker

1. Add a checker module under `src/donespec/checkers/`.
2. Subclass `Checker`.
3. Return `CheckResult` through `self.result(...)`.
4. Register it in `checkers/registry.py`.
5. Extend `done.schema.json` and `src/donespec/schemas/done.schema.json`.
6. Add tests.
7. Add README documentation.

## Design rules

- No LLM calls in core validation.
- No network calls except explicit `http_check`.
- No dashboard in MVP.
- No database.
- No hidden state.
- Fail clearly.
- Prefer deterministic checks over clever checks.
