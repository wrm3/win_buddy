# session-start.ps1 - Cursor hook for session initialization
# Triggered when a new composer conversation is created.
# Injects past agent-memory context so the AI has continuity across sessions.

$inputJson = $input | Out-String

try {
    $eventData    = $inputJson | ConvertFrom-Json
    $sessionId    = $eventData.session_id
    $composerMode = $eventData.composer_mode
} catch {
    $sessionId    = "unknown"
    $composerMode = "unknown"
}

# ── User config check ────────────────────────────────────────────────────────
$userConfigDir  = Join-Path $env:USERPROFILE ".trent"
$userConfigFile = Join-Path $userConfigDir "user_config.json"

$setupNeeded = $false
if (-not (Test-Path $userConfigFile)) {
    try {
        if (-not (Test-Path $userConfigDir)) {
            New-Item -ItemType Directory -Path $userConfigDir -Force | Out-Null
        }
        $machineId = ""
        try {
            $machineId = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Cryptography" `
                          -Name "MachineGuid" -ErrorAction Stop).MachineGuid
        } catch {}
        if (-not $machineId) { $machineId = [System.Guid]::NewGuid().ToString() }

        $cfg = [ordered]@{
            user_id         = "SETUP_NEEDED"
            machine_id      = $machineId
            mcp_url         = "http://localhost:8082"
            created_at      = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
            platform        = "windows"
            created_by      = "session-start.ps1"
            setup_completed = $false
        }
        $cfg | ConvertTo-Json | Set-Content -Path $userConfigFile -Encoding UTF8
    } catch {}
    $setupNeeded = $true
} else {
    try {
        $cfgCheck = Get-Content $userConfigFile -Raw | ConvertFrom-Json
        if ($cfgCheck.user_id -eq "SETUP_NEEDED" -or $cfgCheck.setup_completed -eq $false) {
            $setupNeeded = $true
        }
    } catch {}
}

# ── Reflection reminder (letta-style step-count trigger) ─────────────────────
$setupBanner = ""
if ($setupNeeded) {
    $setupBanner = @"
⚠️  TRENT FIRST-TIME SETUP NEEDED
Your trent user ID has not been configured yet. Please run this command in a terminal:

  powershell -ExecutionPolicy Bypass -File .cursor/hooks/trent-setup-user.ps1

You can use your email, a nickname, or anything you like. This only needs to be done once.
AI memory features will work but sessions won't be linked to a named user until setup is complete.

---
"@
}

$reflectionBanner = ""
$reflectionFile   = ".trent/logs/pending_reflection.json"
if (Test-Path $reflectionFile) {
    try {
        $reflData    = Get-Content $reflectionFile -Raw | ConvertFrom-Json
        $sessionSize = 0
        if ($reflData.turn_count)  { $sessionSize = [int]$reflData.turn_count }
        elseif ($reflData.loop_count) { $sessionSize = [int]$reflData.loop_count }

        if ($sessionSize -ge 5) {
            $topicHint = ""
            if ($reflData.recent_topics -and $reflData.recent_topics.Count -gt 0) {
                $topicHint = "`nSession covered (rough summary from first/last messages):`n"
                foreach ($t in $reflData.recent_topics) { $topicHint += "  - $t`n" }
            }

            $reflectionBanner = @"
## 🧠 Memory Check Reminder
Your previous session had $sessionSize turns.$topicHint
Before starting new work, briefly review and call **``memory_capture_insight``** for anything worth preserving:

- **procedure** — how to do something (deploy, test, git workflow)
- **preference** — user preferences (code style, naming, formatting)
- **correction** — mistakes to avoid next time
- **decision** — architectural choices + rationale
- **context** — project background worth remembering

Keep captures concise (1-3 sentences each). Skip trivial exchanges.

---
"@
        }
        Remove-Item $reflectionFile -ErrorAction SilentlyContinue
    } catch {
        Remove-Item $reflectionFile -ErrorAction SilentlyContinue
    }
}

$additionalContext = "${setupBanner}${reflectionBanner}trent task management system is active. Check .trent/TASKS.md for current tasks."

# ── Fallback Drain ────────────────────────────────────────────────────────────
$fallbackFile = ".trent/memory_fallback.jsonl"
if (Test-Path $fallbackFile) {
    try {
        $mcpUrlFallback = "http://localhost:8082"
        $userConfigPathFallback = Join-Path $env:USERPROFILE ".trent\user_config.json"
        if (Test-Path $userConfigPathFallback) {
            try {
                $ucFallback = Get-Content $userConfigPathFallback -Raw | ConvertFrom-Json
                if ($ucFallback.mcp_url) { $mcpUrlFallback = $ucFallback.mcp_url.TrimEnd("/") }
            } catch {}
        }

        Invoke-WebRequest -Uri "$mcpUrlFallback/memory/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop | Out-Null

        $lines = Get-Content $fallbackFile
        $failedLines = @()
        foreach ($line in $lines) {
            $line = $line.Trim()
            if (-not $line) { continue }
            try {
                $headers = @{ "Content-Type" = "application/json" }
                Invoke-WebRequest -Uri "$mcpUrlFallback/memory/ingest" -Method POST -Body $line -Headers $headers -UseBasicParsing -TimeoutSec 30 -ErrorAction Stop | Out-Null
            } catch {
                $failedLines += $line
            }
        }

        if ($failedLines.Count -eq 0) {
            Remove-Item $fallbackFile -ErrorAction SilentlyContinue
        } else {
            Set-Content -Path $fallbackFile -Value ($failedLines -join "`n") -Encoding UTF8
        }
    } catch {}
}

# ── Memory Context Retrieval ─────────────────────────────────────────────────
$projectIdFile = ".trent/.project_id"
if (Test-Path $projectIdFile) {
    $projectId = (Get-Content $projectIdFile -Raw).Trim()
    if ($projectId -ne "") {
        try {
            $mcpUrl = "http://localhost:8082"
            $userConfigPath = Join-Path $env:USERPROFILE ".trent\user_config.json"
            if (Test-Path $userConfigPath) {
                try {
                    $userConfig = Get-Content $userConfigPath -Raw | ConvertFrom-Json
                    if ($userConfig.mcp_url) { $mcpUrl = $userConfig.mcp_url.TrimEnd("/") }
                } catch {}
            }

            $resp = Invoke-WebRequest -Uri "$mcpUrl/memory/context?project_id=$projectId&max_tokens=3000&platform=cursor" -UseBasicParsing -TimeoutSec 5 -ErrorAction Stop
            $body = $resp.Content | ConvertFrom-Json

            if ($body.success -and $body.context -ne "") {
                $additionalContext = @"
$($body.context)

---
trent task management system is active. Check .trent/TASKS.md for current tasks.
"@
            }
        } catch {}
    }
}

# ── Vault migration (auto-migrate .trent/vault/ → shared when TRENT_VAULT_PATH set) ──
try {
    . "$PSScriptRoot\vault-resolve.ps1"
    $localVault = Join-Path (Get-Location).Path ".trent\vault"
    if ($VaultPath -and $VaultPath -ne $localVault -and (Test-Path $localVault)) {
        $localFiles = Get-ChildItem -Path $localVault -Recurse -Filter "*.md" -ErrorAction SilentlyContinue
        if ($localFiles -and $localFiles.Count -gt 0) {
            $migrated = 0
            foreach ($file in $localFiles) {
                $relPath = $file.FullName.Substring($localVault.Length).TrimStart('\', '/')
                $destPath = Join-Path $VaultPath $relPath
                $destDir = Split-Path $destPath -Parent
                if (-not (Test-Path $destDir)) {
                    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
                }
                if (-not (Test-Path $destPath)) {
                    Copy-Item -Path $file.FullName -Destination $destPath -Force
                    $migrated++
                } else {
                    $srcHash = (Get-FileHash $file.FullName -Algorithm SHA256).Hash
                    $dstHash = (Get-FileHash $destPath -Algorithm SHA256).Hash
                    if ($srcHash -ne $dstHash) {
                        Copy-Item -Path $file.FullName -Destination $destPath -Force
                        $migrated++
                    }
                }
            }
            if ($migrated -gt 0) {
                Remove-Item -Path $localVault -Recurse -Force -ErrorAction SilentlyContinue
                $additionalContext += "`n`n## Vault Auto-Migration`nMigrated $migrated notes from .trent/vault/ to $VaultPath. Local vault cleaned up.`n"
            }
        }
    }
} catch {}

# ── Response ─────────────────────────────────────────────────────────────────
$response = @{
    continue           = $true
    additional_context = $additionalContext
}

$response | ConvertTo-Json -Compress
exit 0
