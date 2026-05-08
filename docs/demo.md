# Demo experience

This demo proves the core DoneSpec claim:

```text
AI agents say tasks are done.
DoneSpec verifies they actually are.
```

The story is intentionally small:

1. A temporary project is created.
2. `done.json` protects `README.md` with `file_not_modified`.
3. A simulated agent modifies that forbidden file.
4. DoneSpec detects the violation.
5. Validation fails.
6. The file is restored.
7. DoneSpec validates successfully.

No cloud service, dashboard, agent runtime, database, or LLM dependency is involved.

In this scenario, the file is protected by done.json and any modification must fail validation.

## Why forbidden-file detection matters

AI coding agents often touch more than the requested change. A task can look complete while a protected file, lockfile, generated artifact, release note, or policy document was changed by accident.

`file_not_modified` makes that requirement explicit. If a protected path changes, DoneSpec fails with a deterministic exit code that local shells, git hooks, CI, and agents can all use.

## Run the demo

Windows PowerShell:

```powershell
.\scripts\demo-forbidden-file.ps1
```

Unix and macOS:

```bash
./scripts/demo-forbidden-file.sh
```

Both scripts create a temporary `.tmp-donespec-demo` project, initialize a git baseline, run the failure case, restore the forbidden file, run the passing case, and remove the temporary demo directory when finished.

The cleanup step removes the temporary demo directory after the script exits.

## Expected failure

The failure moment should look like this:

```text
==> Simulating agent modifying forbidden file

==> Running DoneSpec. This is expected to fail.
DoneSpec validation: agent-completion-demo

+ README exists  (0.4ms)
x README was not modified  (31.5ms)
  Forbidden path modified: README.md

Validation failed.
1 check failed.
Exit code: 1
```

On Unicode-capable terminals, DoneSpec may display check and cross status glyphs instead of ASCII fallback symbols.

## Expected pass

After the script restores `README.md`, the same contract passes:

```text
==> Restoring forbidden file

==> Running DoneSpec again. This is expected to pass.
DoneSpec validation: agent-completion-demo

+ README exists  (0.4ms)
+ README was not modified  (28.2ms)

Validation passed. 2 checks passed.
Exit code: 0
```

## What this proves

DoneSpec validates explicit completion contracts, not confidence.

The demo is deterministic, local, and CI-friendly:

- it runs in a local temporary project
- it uses plain `done.json`
- it depends on git status, not hidden state
- it exits non-zero when the protected file changes
- it exits zero after the violation is fixed
- it cleans up temporary files after execution

For a compact terminal transcript, see [demo-transcript.md](demo-transcript.md).

For recording guidance, see [demo-recording.md](demo-recording.md).
