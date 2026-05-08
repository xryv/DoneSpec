# Demo experience

This demo exists to make DoneSpec understandable in under 20 seconds.

The core story:

```text
AI agent says a task is done.
DoneSpec verifies whether it actually is.
```

The most memorable scenario is simple:

```text
1. A file is protected by done.json
2. An agent modifies it anyway
3. DoneSpec detects the violation
4. Validation fails
5. The file is restored
6. Validation passes
```

This is the product.

Not a dashboard.
Not a platform.
Not AI magic.

A deterministic completion gate.

## Demo script

Use this narrative when recording a terminal GIF or short video:

```text
An AI coding agent can sound confident.

But confidence is not completion.

Here, done.json says README.md must not be modified.

Now we simulate an agent changing it.

DoneSpec runs.

It fails.

The agent fixes the violation.

DoneSpec runs again.

It passes.

Done means deterministically verified.
```

## PowerShell demo

Run:

```powershell
.\scripts\demo-forbidden-file.ps1
```

What it does:

```text
creates a temporary git repo
creates a done.json contract
protects README.md from modification
commits a clean baseline
modifies README.md
runs DoneSpec
shows the expected failure
restores README.md
runs DoneSpec again
shows the passing result
```

## Unix demo

Run:

```bash
./scripts/demo-forbidden-file.sh
```

## Expected failure moment

The demo should show a failure similar to:

```text
DoneSpec validation: agent-completion-demo

x README was not modified
  Forbidden path modified: README.md

Validation failed.
1 check failed.
Exit code: 1
```

## Expected success moment

After restoring the forbidden file:

```text
DoneSpec validation: agent-completion-demo

+ README exists
+ README was not modified

Validation passed. 2 checks passed.
Exit code: 0
```

On Unicode-capable terminals, DoneSpec may display status glyphs instead of ASCII fallback symbols.

Both are acceptable.

## Recording guidance

Keep the recording short.

Recommended structure:

```text
0-3s: show done.json contract
3-7s: simulate forbidden edit
7-12s: run DoneSpec and show failure
12-16s: restore file
16-20s: run DoneSpec and show pass
```

## Suggested terminal title

```text
AI said done. DoneSpec said no.
```

## Suggested caption

```text
AI agents should not be trusted because they sound confident.
They should be trusted when deterministic checks pass.
```

## Suggested social copy

```text
AI coding agents need a completion gate.

DoneSpec is a tiny local-first validator that checks whether a task is actually done.

No cloud.
No LLM dependency.
No orchestration platform.

Just done.json + deterministic checks.

Done means deterministically verified.
```

## Why this demo matters

The demo shows the entire value proposition:

```text
agent claim -> contract -> deterministic validation -> trusted result
```

That is DoneSpec.

Small.
Local.
Composable.
Standard-ready.
