---
id: 101
title: 'Implement add todo functionality'
type: feature
status: completed
priority: high
phase: 1
subsystem: todo-widget
concern: feature
project_context: 'Core todo capture flow. Enables the primary use case of quickly adding reminders (target < 3 seconds).'
dependencies: [100]
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
  completed_steps: ["Wired + button to open inline editor", "Enter key saves new item", "Item appended to list immediately"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [todo, add, inline-edit]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 1
---

# Task 101: Implement add todo functionality

## Objective
Allow users to add a new todo item by clicking the "+" button and typing text, confirmed with Enter.

## Acceptance Criteria

- [x] Clicking "+" opens an inline text input
- [x] Pressing Enter saves the item and closes input
- [x] Pressing Escape cancels without saving
- [x] New item appears immediately in the list

## Implementation Notes
- QLineEdit inline editor opened at top of list
- Enter key: call `add_todo(text)`, hide editor
- Escape key: hide editor without saving

## Verification
- [x] Todo appears immediately after Enter
- [x] Escape cancels without adding empty item
