# OpenAI Agents SDK Integration Example

Use DoneSpec as an external deterministic validation command after file modifications.

The agent workflow only needs to call the CLI:

```text
After applying code changes, execute:

donespec validate done.json --strict

Return success only if the command exits with code 0.
If it exits non-zero, treat the task as incomplete and inspect the failure output.
Do not weaken, remove, or bypass DoneSpec checks to make validation pass.
```

No DoneSpec-specific agent runtime is required.
