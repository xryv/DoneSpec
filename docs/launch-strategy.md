# OSS launch strategy

## Positioning

DoneSpec should be positioned as the missing deterministic completion layer for AI coding agents.

Core line:

> Done means deterministically verified.

## Audience

- solo developers using coding agents,
- maintainers reviewing AI-generated PRs,
- small teams adopting agentic coding,
- OSS projects that need reproducible acceptance checks.

## Launch assets

- README with problem framing and fast demo.
- 60-second terminal GIF.
- Example `done.json` for common tasks.
- GitHub Action snippet.
- Comparison against vague agent completion messages.

## First distribution channels

- GitHub Trending target through tight README and examples.
- Hacker News: "Show HN: DoneSpec — deterministic done checks for AI coding agents".
- Reddit: r/programming, r/LocalLLaMA, r/devops, r/opensource.
- X/LinkedIn founder-style launch thread.
- OSS issue templates encouraging contributors to add checkers.

## Avoid at launch

- enterprise dashboard language,
- AI orchestration claims,
- complicated plugin markets,
- cloud accounts,
- metrics that require telemetry.

## Launch roadmap

1. v0.1: CLI + deterministic checks + GitHub Action.
2. v0.2: more checkers, better summaries, examples.
3. v0.3: generated schema docs and shell completions.
4. v0.4: MCP server prototype.
5. v1.0: stable schema, stable checker contract, stable action.
