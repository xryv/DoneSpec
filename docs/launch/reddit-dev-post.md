# Reddit/dev community post draft

Title:

```text
I built a tiny CLI that checks whether AI coding agents actually finished the task
```

Post:

AI agents say tasks are done.
DoneSpec verifies they actually are.

I built DoneSpec to handle a practical failure mode I kept seeing with AI coding agents: the agent says the task is complete, but a deterministic check proves it is not.

Examples:

- tests still fail
- a required file was not created
- a protected file was modified
- expected documentation was skipped
- a local endpoint does not respond

DoneSpec uses a `done.json` contract. You define the checks that prove completion for the task, then run:

```bash
pip install donespec
donespec init --yes
donespec validate done.json --strict
```

If validation fails, the task is not done. The agent needs to fix the issue and run validation again before claiming completion.

The tool is intentionally local-first: no cloud service, no hidden network calls for normal validation, no LLM dependency, no agent runtime, and no orchestration layer. It uses plain files and exit codes, so it works in local terminals, git hooks, and CI.

DoneSpec does not replace tests, CI, or human review. It validates explicit contracts, not semantic correctness.

I would especially like feedback from people using Codex, Cursor, Claude Code, Aider, OpenAI Agents SDK workflows, or any setup where agents open PRs and CI needs a clear completion gate.
