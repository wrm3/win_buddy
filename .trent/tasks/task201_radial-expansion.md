---
id: 201
title: 'Implement radial expansion animation'
type: feature
status: completed
priority: high
phase: 2
subsystem: hex-launcher
concern: feature
project_context: 'Radial expansion reveals toolbar buttons around the hex. Core UX of the launcher — delivers G-02 (< 2 clicks to launch app).'
dependencies: [200]
ai_safe: true
blast_radius: low
requires_verification: true
requires_solo_agent: false
spec_version: 1
spec_last_verified: "2026-02-03"
allow_spec_update: false
claimed_by: null
claimed_at: null
estimated_duration_minutes: 90
claim_ttl_minutes: 135
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
  completed_steps: ["Calculated radial positions for toolbar buttons", "QPropertyAnimation for expand/collapse", "Buttons fade in/out during animation"]
  remaining_steps: []
  checkpoint_note: null
execution_cost:
  model_used: null
  input_tokens: null
  output_tokens: null
  estimated_cost_usd: null
  review_cost_usd: null
  total_cost_usd: null
tags: [animation, radial, launcher]
created_date: "2026-02-03"
completed_date: "2026-02-03"
rules_version: "6.0.0"
actual_files_changed: 2
---

# Task 201: Implement radial expansion animation

## Objective
Animate toolbar buttons expanding outward from the central hex button when clicked/hovered.

## Acceptance Criteria

- [x] Toolbar buttons expand radially from the hex center
- [x] Smooth animation (no instant jump)
- [x] Buttons collapse back when hex is clicked again or focus is lost
- [x] Multiple toolbars displayed as separate arcs or rings

## Implementation Notes
- Calculate angles evenly distributed across 360° (or a configured arc)
- Use `QPropertyAnimation` on button position properties
- Collapse on second click or `leaveEvent`

## Verification
- [x] Expansion animation visible and smooth
- [x] Collapse returns buttons to hidden state
