---
id: 5
title: 'Implement auto-start on Windows boot'
type: feature
status: completed
priority: medium
phase: 0
subsystem: core
concern: feature
project_context: 'Auto-start ensures WinBuddy is available immediately after boot without manual launching. Supports G-01 (always-visible widget).'
dependencies: [2]
ai_safe: true
blast_radius: low
requires_verification: true
requires_solo_agent: false
spec_version: 1
spec_last_verified: "2026-02-03"
allow_spec_update: false
claimed_by: null
claimed_at: null
estimated_duration_minutes: 30
claim_ttl_minutes: 45
claim_expires_at: null
last_heartbeat: null
verified_by: "human"
verified_date: "2026-02-03"
evidence_of_completion:
  type: manual_check
  path: null
failure_history: []
execution_progress:
  last_checkpoint: "completed"
  checkpoint_date: "2026-02-03"
  completed_steps: ["Read Registry HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run", "Wrote WinBuddy entry on first launch", "Added toggle in settings menu"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [auto-start, registry, windows]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 1
---

# Task 5: Implement auto-start on Windows boot

## Objective
Register WinBuddy in the Windows Registry to launch automatically when the user logs in.

## Acceptance Criteria

- [x] WinBuddy appears in Windows startup programs
- [x] Application launches automatically on next login
- [x] Auto-start can be toggled off via settings/tray menu

## Implementation Notes
- Used `winreg` to write to `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- Key name: `WinBuddy`
- Value: full path to the executable/script

## Verification
- [x] Key exists in Registry after first launch
- [x] App starts on next login (tested manually)
