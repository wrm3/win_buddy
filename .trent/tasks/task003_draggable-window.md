---
id: 3
title: 'Implement draggable window functionality'
type: feature
status: pending
priority: high
phase: 0
subsystems: [ui]
project_context: 'Allow user to drag the widget anywhere on screen'
dependencies: [2]
---

# Task: Implement draggable window functionality

## Objective
Allow the user to click and drag the widget to any position on the screen(s).

## Acceptance Criteria
- [ ] Click and drag moves the window
- [ ] Works on multi-monitor setups
- [ ] Smooth movement without lag
- [ ] Position saved for restoration

## Implementation Notes
- Override mousePressEvent to capture start position
- Override mouseMoveEvent to calculate delta and move window
- Override mouseReleaseEvent to end drag
- Use self.move() with calculated position
- Track drag state with a flag

## Verification
- [ ] Drag widget to all corners of screen
- [ ] Drag widget to secondary monitor
- [ ] Movement is smooth
