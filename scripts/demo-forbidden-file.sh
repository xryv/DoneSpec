#!/usr/bin/env bash
set -euo pipefail

ORIGINAL_LOCATION="$(pwd)"
DEMO_ROOT="$ORIGINAL_LOCATION/.tmp-donespec-demo"

cleanup_demo() {
        rm -rf "$DEMO_ROOT"
}

trap cleanup_demo EXIT

rm -rf "$DEMO_ROOT"
mkdir -p "$DEMO_ROOT"

cd "$DEMO_ROOT"

echo ""
echo "==> Creating temporary DoneSpec demo project"

git init >/dev/null
git config user.email "demo@example.com"
git config user.name "DoneSpec Demo"

cat > README.md <<'EOF'
# Demo Project

Stable baseline.
EOF

cat > done.json <<'JSON'
{
  "$schema": "done.schema.json",
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
JSON

donespec schema --write done.schema.json --force

git add README.md done.json done.schema.json
git commit -m "baseline demo contract" >/dev/null

echo ""
echo "==> Baseline contract"
cat done.json

echo ""
echo "==> Simulating agent modifying forbidden file"
printf "\nAgent edited this forbidden file.\n" >> README.md

echo ""
echo "==> Running DoneSpec. This is expected to fail."
set +e
donespec validate done.json --strict
STATUS="$?"
set -e

if [ "$STATUS" -eq 0 ]; then
    echo "Expected DoneSpec validation to fail after forbidden file modification."
    exit 1
fi

echo ""
echo "==> Restoring forbidden file"
git checkout -- README.md

echo ""
echo "==> Running DoneSpec again. This is expected to pass."
donespec validate done.json --strict

echo ""
echo "Demo complete."

