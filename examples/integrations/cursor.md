# Cursor Integration Example

Keep `done.json` in the project root and associate it with `done.schema.json` for editor autocomplete.

Paste this into Cursor project rules:

```text
This repository uses DoneSpec for deterministic completion validation.

Before marking a task as done, run:

donespec validate done.json --strict

If validation fails, continue working until it passes.
Do not weaken, remove, or bypass checks in done.json unless explicitly requested.
```

Run the command from Cursor's integrated terminal or a VS Code-style task.
