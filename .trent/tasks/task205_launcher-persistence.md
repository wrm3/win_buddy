---
id: 205
title: 'Connect launcher to storage persistence'
type: feature
status: pending
priority: high
phase: 2
subsystems: [ui, storage]
project_context: 'Ensure launcher configuration survives restart'
dependencies: [6, 202, 203, 204]
---

# Task: Connect launcher to storage persistence

## Objective
Wire up the hex launcher to storage so all toolbars and shortcuts persist.

## Acceptance Criteria
- [ ] Toolbars load from storage on startup
- [ ] Add/rename/delete toolbar saves immediately
- [ ] Add/remove shortcut saves immediately
- [ ] Nested structure persisted correctly

## Implementation Notes
- StorageManager provides load_launchers() and save_launchers()
- Data structure:
  ```json
  {
    "toolbars": [
      {
        "id": "uuid",
        "name": "Dev Tools",
        "color": "#3498db",
        "items": [
          {"type": "shortcut", "name": "VS Code", "path": "..."},
          {"type": "toolbar", "id": "sub-uuid", ...}
        ]
      }
    ]
  }
  ```
- Save after every modification

## Verification
- [ ] Add toolbar, restart - still there
- [ ] Add shortcut, restart - still there
- [ ] Nested structure persists correctly
- [ ] First run with no file - empty launchers work
