# OSS launch preparation

This document prepares DoneSpec for public open-source launch messaging.

The goal is not hype.

The goal is immediate comprehension.

Draft launch assets live in [docs/launch/README.md](launch/README.md).

## Primary message

```text
AI agents say tasks are done.

DoneSpec verifies they actually are.
```

## One-line description

```text
DoneSpec is the deterministic completion layer for AI coding agents.
```

## Short description

DoneSpec is a tiny local-first CLI that validates whether an AI coding agent actually completed a task.

It uses a `done.json` contract, deterministic checks, and normal exit codes.

No cloud service.

No LLM dependency.

No agent runtime.

Just explicit completion validation.

## Problem

AI coding agents are increasingly capable, but they can still claim completion when:

- tests fail
- required files are missing
- forbidden files changed
- documentation was skipped
- CI assumptions were weakened
- the task contract was misunderstood

Confidence is not completion.

## Solution

DoneSpec makes completion explicit:

```text
agent output -> done.json contract -> deterministic checks -> pass/fail result
```

If the contract fails, the task is not done.

## Launch tagline options

```text
AI said done. DoneSpec checked.
```

```text
Done means deterministically verified.
```

```text
A tiny completion contract for AI coding agents.
```

```text
The local-first trust layer for agent-written code.
```

```text
Stop trusting agent confidence. Validate completion.
```

## GitHub repository description

```text
Deterministic completion validation for AI coding agents.
```

## PyPI description

```text
DoneSpec is a local-first CLI for validating AI coding agent task completion using deterministic done.json contracts.
```

## README hero copy

```text
AI agents say tasks are done.

DoneSpec verifies they actually are.
```

## Short announcement

DoneSpec v1.0 is a tiny local-first CLI that gives AI coding agents a deterministic completion gate.

Agents can write code.

DoneSpec verifies whether the task is actually complete.

It uses a simple `done.json` contract, deterministic checks, and normal CI-friendly exit codes.

No cloud.

No LLM dependency.

No orchestration platform.

Just:

```bash
donespec validate done.json --strict
```

Done means deterministically verified.

## Longer announcement

AI coding agents are getting better at writing code, but their definition of ?done? is still often conversational.

They may say a task is complete while tests fail, files are missing, forbidden paths changed, or documentation was skipped.

DoneSpec adds a small deterministic layer between agent confidence and human trust.

You define a `done.json` contract.

DoneSpec runs deterministic checks.

CI, humans, and agents all get the same pass/fail result.

It is intentionally boring:

- no database
- no hosted service
- no LLM dependency
- no agent runtime
- no dashboard
- no orchestration layer

Just a local CLI and an explicit completion contract.

```bash
pip install donespec
donespec init --yes
donespec validate done.json --strict
```

AI agents say tasks are done.

DoneSpec verifies they actually are.

## Launch audience

DoneSpec is for:

- developers using AI coding agents
- maintainers reviewing agent-generated PRs
- teams adopting Cursor, Codex, Claude Code, Aider, or similar tools
- CI-heavy engineering teams
- open-source maintainers
- people who want agent work to be inspectable and reproducible

## Avoid these claims

Do not claim DoneSpec:

- makes AI agents reliable by itself
- guarantees code correctness
- replaces tests
- replaces human review
- orchestrates agents
- manages workflows
- stores memory
- understands intent semantically
- uses AI internally

DoneSpec validates explicit contracts.

That is enough.

## Suggested launch checklist

Before public launch:

```text
? README polished
? PyPI release published
? GitHub release published
? demo GIF or terminal recording ready
? docs/demo.md ready
? docs/integrations.md ready
? docs/editor-support.md ready
? docs/cross-platform-verification.md ready
? docs/release-checklist.md ready
? CHANGELOG.md current
? v1.0 release notes drafted
? repository description updated
? repository topics added
? social announcement drafted
? Hacker News title drafted
? Reddit/dev community post drafted
```

## Suggested repository topics

```text
ai-agents
developer-tools
cli
ci
automation
validation
testing
json-schema
ai-coding
local-first
```

## Suggested Hacker News title

```text
Show HN: DoneSpec ? deterministic completion validation for AI coding agents
```

## Suggested Reddit/dev title

```text
I built a tiny CLI that checks whether AI coding agents actually finished the task
```

## Final launch principle

DoneSpec should not look like a startup platform.

It should look like a missing infrastructure primitive.
