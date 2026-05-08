# Changelog

All notable changes to DoneSpec are documented here.

DoneSpec follows semantic versioning.

The project goal is to remain a tiny, local-first, deterministic completion layer for AI coding agents.

## Unreleased

### Stabilization

- Prepare v1.0 release engineering.
- Strengthen release checklist documentation.
- Keep the core minimal, deterministic, and composable.
- Avoid platform expansion, orchestration, cloud services, dashboards, databases, agent runtimes, memory layers, plugin systems, or LLM dependencies.

## 0.7.0

### Added

- Added the Contract Authoring Layer.
- Added `donespec add-check`.
- Added safe check insertion into existing `done.json` files.
- Added validation of updated contracts before writing changes.
- Added authoring documentation.
- Added authoring tests for file checks, command checks, duplicate names, missing required fields, invalid regex patterns, and strict validation failures.

### Improved

- Improved the workflow for agents and humans extending completion contracts.
- Reduced the need to manually edit JSON for common DoneSpec changes.

## 0.6.0

### Added

- Added `donespec explain`.
- Added human-readable contract explanation output.
- Added machine-readable JSON explanation output.
- Added strict explanation mode.
- Added explanation documentation and tests.

### Improved

- Improved contract inspectability before execution.
- Improved agent and reviewer workflows.

## 0.5.0

### Added

- Added strict semantic validation mode with `donespec validate --strict`.
- Added strict validation for empty contracts, unnamed checks, duplicate check names, duplicate check IDs, invalid regex patterns, absolute paths, and parent traversal paths.
- Added strict validation documentation and tests.

### Improved

- Strengthened DoneSpec as a deterministic completion gate for serious agent workflows.

## 0.4.0

### Added

- Added schema command support.
- Added packaged JSON Schema export.
- Added local schema generation.
- Added schema documentation and tests.

### Improved

- Improved editor and tool integration through `done.schema.json`.

## 0.3.0

### Added

- Added template support.
- Added project templates for generic, Python, Node, docs, and API workflows.
- Added templates command and documentation.

### Improved

- Improved onboarding for common project types.

## 0.2.0

### Added

- Added project initialization workflow.
- Added `donespec init`.
- Added generated agent instructions.
- Added VS Code task generation.
- Added git hook installer scripts.
- Added doctor command.

### Improved

- Improved first-run project setup.

## 0.1.1

### Improved

- Improved initial packaging, metadata, and release readiness.

## 0.1.0

### Added

- Initial MVP.
- Added `donespec validate done.json`.
- Added deterministic validation engine.
- Added checker registry.
- Added supported checks:
  - `command`
  - `file_exists`
  - `regex_in_file`
  - `regex_absent`
  - `file_not_modified`
  - `http_check`
- Added human-readable CLI output.
- Added JSON output.
- Added JSON Schema validation.
- Added GitHub Action integration.
- Added examples.
- Added self-validation contract.
- Added test suite.

### Philosophy

- Done means deterministically verified.
