---
id: 1
title: 'Project setup with UV and PyQt6'
type: feature
status: completed
priority: critical
phase: 0
subsystem: core
concern: feature
project_context: 'Initialize Python project with UV package manager and PyQt6 dependencies. Supports G-01 (always-visible widget) by establishing the entire application foundation.'
dependencies: []
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
  completed_steps: ["Created pyproject.toml", "Added PyQt6 dependency", "Created venv with UV", "Created main.py entry point", "Verified window launches"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [setup, uv, pyqt6]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 3
---

# Task 1: Project setup with UV and PyQt6

## Objective
Create the project structure with UV as package manager and install PyQt6 for cross-platform GUI development.

## Context
Foundation task — all other tasks depend on this. Establishes the Python environment, dependency management, and application entry point.

## Acceptance Criteria

- [x] pyproject.toml created with project metadata
- [x] PyQt6 added as dependency
- [x] Virtual environment created via UV
- [x] main.py entry point created
- [x] Basic "Hello World" window launches

## Implementation Notes
- Used `uv init` to create project
- Added PyQt6 >= 6.6.0
- Created src/winbuddy/ package structure
- Entry point in main.py at root

## Verification
- [x] `uv run python main.py` launches window
- [x] No import errors
