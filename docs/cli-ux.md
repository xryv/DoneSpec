# CLI UX principles

DoneSpec CLI output is designed to be boring in the best sense: short, stable, deterministic, and easy to trust in a terminal or CI log.

## Principles

- Minimal human output for fast review.
- Deterministic results from explicit `done.json` contracts.
- Stable exit codes for shell scripts, git hooks, and CI.
- No hidden network calls.
- Local-first execution.
- Windows-safe output with ASCII fallback on legacy output streams.
- JSON output for automation.
- Human output for quick inspection.
- Strict mode for release gates and serious agent workflows.

DoneSpec should not explain more than the operator needs at the point of execution. If validation fails, the output should identify the failing check and preserve a deterministic exit code.

## Exit codes

```text
0  validation passed
1  validation completed and one or more checks failed
2  spec or runtime error prevented validation from completing
```

## Human output

```bash
donespec validate done.json
```

```text
DoneSpec validation: ship-safe-change

+ README exists  (0.4ms)
+ tests pass  (812.4ms)

Validation passed. 2 checks passed.
Exit code: 0
```

Use human output for local review, pull request logs, and agent terminal sessions.

## Strict release gate

```bash
donespec validate done.json --strict
```

Strict mode validates contract hygiene before checks run. It catches duplicate check names, duplicate check IDs, invalid regex patterns, empty contracts, unsafe absolute paths, and parent traversal paths.

## Explain without executing checks

```bash
donespec explain done.json
```

Use this when an agent or reviewer needs to inspect the completion contract before running it.

```bash
donespec explain done.json --json
```

Use JSON output when another tool needs a parseable contract summary.

## Project readiness

```bash
donespec doctor
```

`doctor` checks whether a repository has the expected DoneSpec files and integrations. It is a local inspection command; it does not contact external services.

## Safe authoring

```bash
donespec add-check done.json --type file_exists --name "README exists" --path README.md
```

`add-check` validates the updated contract before writing it. Errors should remain clear and actionable, such as duplicate check names, invalid groups, or missing required fields.

## JSON output

Machine-readable output is available where automation needs it:

```bash
donespec validate done.json --json
donespec explain done.json --json
donespec doctor --json
donespec templates --json
```

JSON output is intended for scripts, CI steps, editor integrations, and agent tooling. It should remain parseable and avoid human-only formatting.

## Windows-safe output

Human output uses Unicode status symbols when the stream supports them. On legacy Windows streams such as `cp1252`, DoneSpec falls back to ASCII status symbols:

```text
+ passing check
x failing check
```

This keeps CLI output usable in local terminals, GitHub Actions, redirected logs, and older Windows environments.
