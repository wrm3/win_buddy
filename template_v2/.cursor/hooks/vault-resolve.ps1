# vault-resolve.ps1 — Resolve the vault path and project identity.
# Source this from other hooks: . "$PSScriptRoot\vault-resolve.ps1"
#
# After sourcing, these variables are available:
#   $VaultPath   — resolved vault root (shared or local)
#   $ProjectId   — UUID from .trent/.project_id (or "unknown")
#   $ProjectName — folder name of the project root
#   $ProjectDir  — project-specific vault subfolder path

$VaultPath   = $null
$ProjectId   = "unknown"
$ProjectName = Split-Path (Get-Location).Path -Leaf

# Read project ID
$pidFile = Join-Path (Get-Location).Path ".trent\.project_id"
if (Test-Path $pidFile) {
    $ProjectId = (Get-Content $pidFile -Raw).Trim()
}

# Resolve vault path from .env or fall back to local
$envFile = Join-Path (Get-Location).Path ".env"
if (Test-Path $envFile) {
    $match = Select-String -Path $envFile -Pattern '^\s*TRENT_VAULT_PATH\s*=\s*(.+)' | Select-Object -First 1
    if ($match) {
        $candidate = $match.Matches[0].Groups[1].Value.Trim().Trim('"').Trim("'")
        if ($candidate -and $candidate -ne '') {
            $VaultPath = $candidate
        }
    }
}

if (-not $VaultPath) {
    $VaultPath = Join-Path (Get-Location).Path ".trent\vault"
}

if (-not (Test-Path $VaultPath)) {
    New-Item -ItemType Directory -Path $VaultPath -Force | Out-Null
}

# Project-specific vault directory (keyed by project_id for uniqueness)
$ProjectDir = Join-Path $VaultPath "projects\${ProjectId}_${ProjectName}"
