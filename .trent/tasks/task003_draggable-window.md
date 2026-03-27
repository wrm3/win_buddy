---
id: 3
title: 'Implement draggable window functionality'
type: feature
status: completed
priority: high
phase: 0
subsystem: core
concern: feature
project_context: 'Allows users to position WinBuddy anywhere on screen. Supports G-01 (always-visible widget in user-preferred position).'
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
  completed_steps: ["Implemented mousePressEvent", "Implemented mouseMoveEvent", "Position saved to storage"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [drag, mouse-events]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 1
---

# Task 3: Implement draggable window functionality

## Objective
Allow users to click-and-drag the WinBuddy window to any position on the screen, with position persisted across restarts.

## Acceptance Criteria

- [x] Window can be dragged by clicking and holding anywhere on the widget body
- [x] Window position is remembered after restart
- [x] Dragging does not interfere with button clicks inside the widget

## Implementation Notes
- Override `mousePressEvent` to record drag start position
- Override `mouseMoveEvent` to call `move()` with offset
- Save final position via storage manager on `mouseReleaseEvent`

## Verification
- [x] Widget moves smoothly when dragged
- [x] Position restored correctly after restart
