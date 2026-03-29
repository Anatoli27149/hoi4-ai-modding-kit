$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$skillSource = Join-Path $repoRoot "skills\hoi4-modding"
$codexHome = Join-Path $env:USERPROFILE ".codex"
$skillTarget = Join-Path $codexHome "skills\hoi4-modding"

if (-not (Test-Path $codexHome)) {
    throw "Codex home not found at $codexHome"
}

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillTarget) | Out-Null

if (Test-Path $skillTarget) {
    Remove-Item -Recurse -Force $skillTarget
}

Copy-Item -Recurse -Force $skillSource $skillTarget

Write-Host "Installed skill to $skillTarget"
Write-Host ""
Write-Host "Add this MCP block to your Codex config if it is not already present:"
Write-Host '[mcp_servers.hoi4-modding]'
Write-Host 'command = "python"'
Write-Host 'args = ["-m", "hoi4_ai_modding.mcp_server"]'
