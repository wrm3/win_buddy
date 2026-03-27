---
id: 104
title: 'Connect todo list to storage persistence'
type: feature
status: pending
priority: high
phase: 1
subsystems: [ui, storage]
project_context: 'Ensure todos survive app restarts'
dependencies: [6, 100, 101, 102, 103]
---

# Task: Connect todo list to storage persistence

## Objective
Wire up the todo list UI to the storage manager so all changes persist.

## Acceptance Criteria
- [ ] Todos load from storage on startup
- [ ] Add/edit/delete saves immediately
- [ ] No data loss on crash (atomic saves)
- [ ] Works with empty initial state

## Implementation Notes
- StorageManager provides load_todos() and save_todos()
- TodoList widget calls storage on any change
- Load in __init__, save after each modification
- Use simple list of dicts: [{id, text, created_at}]

## Verification
- [ ] Add todos, restart - they're still there
- [ ] Edit todo, restart - edit persisted
- [ ] Delete todo, restart - deletion persisted
- [ ] First run with no file - empty list works
