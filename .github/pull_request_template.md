# Pull request

## Summary

Describe the change.

## Why this change is needed

Explain the problem this PR solves.

## Type of change

- [ ] Bug fix
- [ ] Documentation
- [ ] CLI improvement
- [ ] Schema improvement
- [ ] Test improvement
- [ ] Release / packaging improvement

## DoneSpec philosophy check

This PR preserves DoneSpec as:

- [ ] local-first
- [ ] deterministic
- [ ] small
- [ ] composable
- [ ] free from LLM dependencies
- [ ] not an orchestration platform
- [ ] not an AI framework
- [ ] not a hosted service

## Validation

Run these before requesting review:

```bash
python -m ruff check .
python -m ruff format --check .
python -m pytest -q
donespec validate done.json
donespec validate done.json --strict
```

## Validation result

- [ ] `ruff check` passed
- [ ] `ruff format --check` passed
- [ ] `pytest` passed
- [ ] `donespec validate done.json` passed
- [ ] `donespec validate done.json --strict` passed

## Notes

Add anything reviewers should know.
