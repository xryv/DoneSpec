# Long announcement draft

AI agents say tasks are done.
DoneSpec verifies they actually are.

DoneSpec is the deterministic completion layer for AI coding agents.

AI coding agents can produce useful code, but agent confidence is not completion. A task can be summarized as finished while tests fail, files are missing, forbidden paths changed, documentation was skipped, or CI assumptions were weakened.

DoneSpec adds a small explicit contract between agent output and completion.

You define a `done.json` file with deterministic checks:

- required files exist
- commands pass
- expected text appears in files
- forbidden text is absent
- protected files were not modified
- local HTTP endpoints respond as expected

Then the agent, a human, a git hook, or CI runs:

```bash
donespec validate done.json --strict
```

If validation fails, the task is not done. The issue must be fixed and validation must run again.

Because the contract is just a local JSON file and the CLI uses normal exit codes, DoneSpec fits into existing workflows: terminal sessions, pull requests, GitHub Actions, pre-push hooks, and AI coding agent instructions.

DoneSpec stays small on purpose. It is not an orchestration platform, AI framework, SaaS, agent runtime, workflow engine, memory layer, or LLM tool. It does not replace tests, CI, or human review.

It validates explicit contracts, not semantic correctness.

DoneSpec is for developers and maintainers using tools like Codex, Claude Code, Cursor, Aider, OpenAI Agents SDK workflows, and other coding agents who want a deterministic completion gate before accepting agent work.

Quickstart:

```bash
pip install donespec
donespec init --yes
donespec validate done.json --strict
```
