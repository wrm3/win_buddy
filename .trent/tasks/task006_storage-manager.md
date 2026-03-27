---
id: 6
title: 'Create JSON storage manager'
type: feature
status: pending
priority: high
phase: 0
subsystems: [storage]
project_context: 'Centralized data persistence for todos, shortcuts, and settings'
dependencies: [1]
---

# Task: Create JSON storage manager

## Objective
Create a storage manager class that handles all data persistence using JSON files.

## Acceptance Criteria
- [ ] StorageManager class with load/save methods
- [ ] Separate files for: settings, todos, launchers
- [ ] Auto-creates data directory if missing
- [ ] Handles corrupt/missing files gracefully
- [ ] Saves on changes, loads on startup

## Implementation Notes
- Store in %APPDATA%/WinBuddy/ on Windows
- Use pathlib for cross-platform paths
- Use json module for serialization
- Create default data structures if files missing
- Add logging for debug purposes

## Data Files
- settings.json: window position, auto-start preference
- todos.json: list of todo items
- launchers.json: toolbar and shortcut configuration

## Verification
- [ ] First run creates data directory
- [ ] Data persists after restart
- [ ] Deleting file recreates defaults
- [ ] Invalid JSON handled gracefully
