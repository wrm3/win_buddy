---
id: 4
title: 'Add system tray integration'
type: feature
status: pending
priority: high
phase: 0
subsystems: [system-integration]
project_context: 'Enable minimize to system tray and restore functionality'
dependencies: [2]
---

# Task: Add system tray integration

## Objective
Integrate with Windows system tray so the widget can be hidden and restored easily.

## Acceptance Criteria
- [ ] System tray icon appears when app runs
- [ ] Clicking X minimizes to tray (not exits)
- [ ] Left-click tray icon restores window
- [ ] Right-click tray icon shows context menu
- [ ] Context menu has "Show", "Exit" options

## Implementation Notes
- Use QSystemTrayIcon
- Create QMenu for right-click context menu
- Override closeEvent to hide instead of close
- Connect tray icon activated signal for left-click
- Use a custom icon (or default app icon initially)

## Verification
- [ ] Click X - window hides, tray icon visible
- [ ] Click tray icon - window reappears
- [ ] Right-click tray - menu shows
- [ ] Click Exit - app actually closes
