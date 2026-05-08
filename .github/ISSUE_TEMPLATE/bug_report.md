---
name: Bug report
about: Report a reproducible DoneSpec bug
title: "[Bug]: "
labels: bug
assignees: ""
---

## What happened?

Describe the bug clearly.

## Expected behavior

What should DoneSpec have done?

## Actual behavior

What happened instead?

## Reproduction steps

```bash
# commands here
```

## DoneSpec version

```bash
donespec --version
```

## Environment

- OS:
- Python version:
- Shell:
- Installation method: pip / local wheel / source

## Relevant output

```text
paste output here
```

## Contract file

If relevant, include a minimal `done.json` that reproduces the issue.

```json
{}
```

## Validation result

Please run:

```bash
donespec validate done.json --strict
```

and include the output.
