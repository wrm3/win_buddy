---
id: 200
title: 'Design and create central hex button'
type: feature
status: pending
priority: critical
phase: 2
subsystems: [ui]
project_context: 'The central trigger for the radial launcher'
dependencies: [2]
---

# Task: Design and create central hex button

## Objective
Create a hexagonal button that serves as the central hub for the launcher.

## Acceptance Criteria
- [ ] Hexagonal shape button
- [ ] Positioned below the todo list
- [ ] Hover state changes appearance
- [ ] Click triggers toolbar expansion
- [ ] Clean, modern look

## Implementation Notes
- Use QPainterPath to draw hexagon
- Override paintEvent for custom shape
- Use stylesheet for colors/hover effects
- OR use QPushButton with hex mask
- Consider using SVG icon

## Verification
- [ ] Button is clearly hexagonal
- [ ] Hover changes color/style
- [ ] Click registered correctly
- [ ] Looks good with todo list above
