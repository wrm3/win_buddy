---
id: 201
title: 'Implement radial expansion animation'
type: feature
status: pending
priority: high
phase: 2
subsystems: [ui]
project_context: 'Animate toolbar buttons expanding in arc from center hex'
dependencies: [200]
---

# Task: Implement radial expansion animation

## Objective
When user hovers or clicks the hex, toolbar buttons expand outward in a radial/arc pattern.

## Acceptance Criteria
- [ ] Toolbar buttons appear around the hex
- [ ] Smooth animation for expansion
- [ ] Buttons arranged in arc or ring
- [ ] Collapse when clicking elsewhere
- [ ] Works with variable number of toolbars

## Implementation Notes
- Calculate positions using trigonometry (sin/cos)
- Use QPropertyAnimation for smooth movement
- Start from center, animate to final positions
- Each toolbar button is a smaller hex or circle
- Parent widget may need to expand temporarily

## Verification
- [ ] Hover/click hex - buttons expand smoothly
- [ ] Buttons arranged evenly around center
- [ ] Click away - buttons collapse
- [ ] Animation is smooth, not jerky
