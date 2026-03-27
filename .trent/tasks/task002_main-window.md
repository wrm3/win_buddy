---
id: 2
title: 'Create main window with frameless, always-on-top behavior'
type: feature
status: completed
priority: critical
phase: 0
subsystem: core
concern: feature
project_context: 'Core window behavior that makes WinBuddy a floating widget. Directly delivers G-01 (always-visible productivity widget).'
dependencies: [1]
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
  completed_steps: ["Set Qt.WindowStaysOnTopHint flag", "Set frameless window flag", "Styled window background"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [window, qt-flags, frameless]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 2
---

# Task 2: Create main window with frameless, always-on-top behavior

## Objective
Create a PyQt6 main window that is frameless (no title bar), always on top of all other windows, and visually styled as a floating widget.

## Acceptance Criteria

- [x] Window has no title bar or system frame
- [x] Window stays on top of all other applications
- [x] Window has semi-transparent or styled background
- [x] Window renders without errors

## Implementation Notes
- Used `Qt.WindowType.FramelessWindowHint` and `Qt.WindowType.WindowStaysOnTopHint`
- Applied stylesheet for dark widget background with rounded corners

## Verification
- [x] Window stays on top when switching to other apps
- [x] No system frame visible
