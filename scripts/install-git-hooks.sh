#!/usr/bin/env sh
set -eu

git config core.hooksPath .githooks

echo ""
echo "DoneSpec Git hooks installed."
echo ""
echo "Active hooks path:"
git config core.hooksPath
echo ""
echo "Pre-push will run:"
echo "  donespec validate done.json"
echo ""
