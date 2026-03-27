---
id: 2
title: 'Create main window with frameless, always-on-top behavior'
type: feature
status: pending
priority: critical
phase: 0
subsystems: [ui, core]
project_context: 'Build the main application window that stays visible above other apps'
dependencies: [1]
---

# Task: Create main window with frameless, always-on-top behavior

## Objective
Create a frameless Qt window that stays on top of all other windows, like the Teams screen share toolbar.

## Acceptance Criteria
- [ ] Window has no standard title bar/frame
- [ ] Window stays on top of all other applications
- [ ] Window has semi-transparent or custom styled background
- [ ] Window appears at a reasonable default position

## Implementation Notes
- Use Qt.WindowType.FramelessWindowHint
- Use Qt.WindowType.WindowStaysOnTopHint
- Use Qt.WindowType.Tool (to avoid taskbar entry)
- Set WA_TranslucentBackground for custom styling
- Apply rounded corners via stylesheet or mask

## Verification
- [ ] Open other apps - widget stays visible
- [ ] Window looks clean without system decorations
