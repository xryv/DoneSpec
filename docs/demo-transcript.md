# Demo transcript

This transcript is a compact terminal flow for the official DoneSpec demo. It is suitable for turning into a GIF, short video, or README preview asset.

```text
$ ./scripts/demo-forbidden-file.sh

==> Creating temporary DoneSpec demo project
Initialized empty Git repository in .tmp-donespec-demo/.git/

==> Baseline contract
{
  "version": "1.0",
  "task_id": "agent-completion-demo",
  "must_pass": [
    {
      "type": "file_exists",
      "name": "README exists",
      "path": "README.md"
    }
  ],
  "must_not": [
    {
      "type": "file_not_modified",
      "name": "README was not modified",
      "path": "README.md"
    }
  ]
}

==> Simulating agent modifying forbidden file
$ printf "\nAgent edited this forbidden file.\n" >> README.md

==> Running DoneSpec. This is expected to fail.
$ donespec validate done.json --strict
DoneSpec validation: agent-completion-demo

+ README exists  (0.4ms)
x README was not modified  (31.5ms)
  Forbidden path modified: README.md

Validation failed.
1 check failed.
Exit code: 1

==> Restoring forbidden file
$ git checkout -- README.md

==> Running DoneSpec again. This is expected to pass.
$ donespec validate done.json --strict
DoneSpec validation: agent-completion-demo

+ README exists  (0.4ms)
+ README was not modified  (28.2ms)

Validation passed. 2 checks passed.
Exit code: 0

Demo complete.
Temporary demo project removed.
```

Core proof:

```text
agent claim -> forbidden file change -> DoneSpec failure -> restore file -> DoneSpec pass
```
