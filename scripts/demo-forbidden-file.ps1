$ErrorActionPreference = "Stop"

$OriginalLocation = Get-Location
$DemoRoot = Join-Path $OriginalLocation ".tmp-donespec-demo"

Remove-Item -Recurse -Force $DemoRoot -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force $DemoRoot | Out-Null

Set-Location $DemoRoot

try {
    Write-Host ""
    Write-Host "==> Creating temporary DoneSpec demo project" -ForegroundColor Cyan

    git init | Out-Null
    git config user.email "demo@example.com"
    git config user.name "DoneSpec Demo"

    Set-Content -Encoding UTF8 README.md "# Demo Project`n`nStable baseline."

    $DoneJson = @(
        "{",
        '  "$schema": "done.schema.json",',
        '  "version": "1.0",',
        '  "task_id": "agent-completion-demo",',
        '  "must_pass": [',
        "    {",
        '      "type": "file_exists",',
        '      "name": "README exists",',
        '      "path": "README.md"',
        "    }",
        "  ],",
        '  "must_not": [',
        "    {",
        '      "type": "file_not_modified",',
        '      "name": "README was not modified",',
        '      "path": "README.md"',
        "    }",
        "  ]",
        "}"
    ) -join [Environment]::NewLine

    Set-Content -Encoding UTF8 done.json $DoneJson

    donespec schema --write done.schema.json --force

    git add README.md done.json done.schema.json
    git commit -m "baseline demo contract" | Out-Null

    Write-Host ""
    Write-Host "==> Baseline contract" -ForegroundColor Cyan
    Get-Content done.json

    Write-Host ""
    Write-Host "==> Simulating agent modifying forbidden file" -ForegroundColor Cyan
    Add-Content -Encoding UTF8 README.md "`nAgent edited this forbidden file."

    Write-Host ""
    Write-Host "==> Running DoneSpec. This is expected to fail." -ForegroundColor Cyan

    $PreviousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    donespec validate done.json --strict
    $FailureExitCode = $LASTEXITCODE
    $ErrorActionPreference = $PreviousErrorActionPreference

    if ($FailureExitCode -eq 0) {
        throw "Expected DoneSpec validation to fail after forbidden file modification."
    }

    Write-Host ""
    Write-Host "==> Restoring forbidden file" -ForegroundColor Cyan
    git checkout -- README.md

    Write-Host ""
    Write-Host "==> Running DoneSpec again. This is expected to pass." -ForegroundColor Cyan
    donespec validate done.json --strict

    if ($LASTEXITCODE -ne 0) {
        throw "Expected DoneSpec validation to pass after restoring README.md."
    }

    Write-Host ""
    Write-Host "Demo complete." -ForegroundColor Green
}
finally {
    Set-Location $OriginalLocation
}
