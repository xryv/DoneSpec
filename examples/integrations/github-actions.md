# GitHub Actions Integration Example

Copy-paste workflow:

```yaml
name: DoneSpec

on:
  pull_request:
  push:

jobs:
  donespec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: xryv/DoneSpec@v0.8.0
      - name: Validate completion contract
        run: donespec validate done.json --strict
```

The action installs DoneSpec. The explicit validation step keeps strict mode visible as the CI gate.
