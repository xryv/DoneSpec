# Aider Integration Example

Keep `done.json` visible while asking Aider to modify the project.

Example prompt:

```text
Make the requested change. Before reporting completion, run:

donespec validate done.json --strict

If validation fails, inspect the failing check, fix the issue, and run validation again.
Do not edit done.json to bypass the intended contract.
```

Do not accept conversational completion without validation.
