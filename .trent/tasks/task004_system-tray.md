---
id: 4
title: 'Add system tray integration'
type: feature
status: completed
priority: high
phase: 0
subsystem: core
concern: feature
project_context: 'System tray lets WinBuddy minimize without closing, keeping it out of the taskbar. Supports G-01 by providing unobtrusive always-available access.'
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
estimated_duration_minutes: 45
claim_ttl_minutes: 68
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
  completed_steps: ["Created QSystemTrayIcon", "Added right-click context menu", "Wired minimize-to-tray on close", "Wired restore on tray icon click"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [tray, system-integration]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 2
---

# Task 4: Add system tray integration

## Objective
Add a system tray icon that allows WinBuddy to minimize to tray instead of closing, with a right-click context menu for restore/exit.

## Acceptance Criteria

- [x] Clicking the window close button minimizes to system tray (does not exit)
- [x] Tray icon is visible in the system tray area
- [x] Right-click on tray icon shows menu with "Show WinBuddy" and "Exit"
- [x] Clicking tray icon restores the window

## Implementation Notes
- Used `QSystemTrayIcon` with a custom icon
- Override `closeEvent` to call `hide()` and show tray icon
- Connect tray icon's `activated` signal to restore window

## Verification
- [x] Minimize to tray works
- [x] Restore from tray works
- [x] Exit via tray menu closes application cleanly
