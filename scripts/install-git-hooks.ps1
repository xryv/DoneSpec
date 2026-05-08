$ErrorActionPreference = "Stop"

git config core.hooksPath .githooks

Write-Host ""
Write-Host "DoneSpec Git hooks installed."
Write-Host ""
Write-Host "Active hooks path:"
git config core.hooksPath
Write-Host ""
Write-Host "Pre-push will run:"
Write-Host "  donespec validate done.json"
Write-Host ""
