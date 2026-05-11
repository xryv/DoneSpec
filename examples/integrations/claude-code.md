# Claude Code Integration Example

Use `CLAUDE.md` to import the shared repository protocol:

```text
@AGENTS.md
```

Add this rule if the repository does not already define one:

```text
Read the task contract in done.json.
Make the requested change.
Run the project's normal tests or checks.
Run `donespec validate done.json --strict`.
Report failures honestly and continue fixing until validation passes.
Do not weaken done.json checks to make validation pass.
```
