---
id: 6
title: 'Create JSON storage manager'
type: feature
status: completed
priority: critical
phase: 0
subsystem: storage
concern: feature
project_context: 'The storage manager is the persistence backbone for all WinBuddy data. Supports G-03 (persistent state across restarts).'
dependencies: [1]
ai_safe: true
blast_radius: medium
blast_radius_reason: "Storage manager is used by both todo-widget and hex-launcher subsystems. Schema changes affect all data."
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
  completed_steps: ["Created StorageManager class", "Implemented load_data/save_data", "Set up %APPDATA%/WinBuddy/ directory creation", "Added schema versioning"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [storage, json, persistence]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 1
---

# Task 6: Create JSON storage manager

## Objective
Create a StorageManager class that reads and writes application data (todos, shortcuts, settings, position) as JSON to the user's AppData directory.

## Acceptance Criteria

- [x] Data directory created at `%APPDATA%/WinBuddy/` if not exists
- [x] `load_data()` returns Python dict from JSON file
- [x] `save_data()` writes dict to JSON file atomically
- [x] Handles missing file gracefully (returns defaults)
- [x] Schema version field included for future migrations

## Implementation Notes
- Used `pathlib.Path` and `os.environ['APPDATA']` for cross-platform path
- Atomic write: write to `.tmp` then rename to avoid corruption
- Default schema returned when file missing or malformed

## Verification
- [x] Data persists across app restarts
- [x] Corrupt/missing file handled without crash
