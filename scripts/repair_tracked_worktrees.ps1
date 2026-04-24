Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$tracked = git ls-files --stage .claude/worktrees
if ($LASTEXITCODE -ne 0) {
    throw "git ls-files failed with exit code $LASTEXITCODE"
}

if (-not $tracked) {
    Write-Host "No tracked entries under .claude/worktrees."
    exit 0
}

$paths = @()
foreach ($line in ($tracked -split "`n")) {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }
    $parts = $line -split "`t", 2
    if ($parts.Length -ne 2) {
        continue
    }
    $paths += $parts[1].Trim()
}

$paths = $paths | Sort-Object -Unique
Write-Host "Removing tracked .claude/worktrees entries from the git index:"
$paths | ForEach-Object { Write-Host "  $_" }

foreach ($path in $paths) {
    git update-index --force-remove -- $path
    if ($LASTEXITCODE -ne 0) {
        throw "git update-index --force-remove failed for '$path' with exit code $LASTEXITCODE"
    }
}

Write-Host ""
Write-Host "Tracked worktree entries removed from index."
Write-Host "Review with: git diff --cached --stat"
Write-Host "If the physical directories are disposable, remove them separately after review."
