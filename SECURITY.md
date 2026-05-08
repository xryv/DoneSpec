# Security policy

DoneSpec is a local-first CLI.

It does not require a cloud service.

It does not require an LLM provider.

It does not send project data to a remote service.

## Supported versions

Security fixes are prioritized for the latest released version.

For best results, use the latest PyPI release:

```bash
python -m pip install --upgrade donespec
```

## Reporting a vulnerability

Please report security issues privately.

Do not open a public issue for a vulnerability.

Use GitHub's private vulnerability reporting if available, or contact the maintainer through the repository owner profile.

Include:

- affected version
- operating system
- reproduction steps
- expected behavior
- actual behavior
- relevant logs
- whether the issue affects local files, command execution, or CI behavior

## Security scope

Relevant security concerns include:

- unsafe path handling
- unintended file modification
- command execution surprises
- schema validation bypasses
- unsafe default behavior
- CI behavior that hides failed validation
- packaging issues
- dependency issues

## Out of scope

DoneSpec does not claim to secure:

- arbitrary user commands inside `done.json`
- third-party CI systems
- AI agent behavior outside the explicit validation contract
- code correctness beyond configured deterministic checks
- malicious repositories designed to execute unsafe commands

DoneSpec validates explicit contracts.

If a contract runs a command, that command should be reviewed like any other project script.

## Design expectation

DoneSpec should remain:

- local-first
- explicit
- deterministic
- inspectable
- dependency-light
- free from hidden network calls
- free from LLM dependencies
