---
id: 103
title: 'Implement delete todo functionality'
type: feature
status: pending
priority: high
phase: 1
subsystems: [ui]
project_context: 'Allow removing completed or unwanted todos'
dependencies: [100]
---

# Task: Implement delete todo functionality

## Objective
Allow users to delete todo items they no longer need.

## Acceptance Criteria
- [ ] Each todo item has delete button (X or trash icon)
- [ ] Click delete removes item immediately
- [ ] No confirmation needed (keeps it fast)
- [ ] Item removed from storage

## Implementation Notes
- Add small X button to right of each item
- On click, remove from list widget
- Emit signal for storage to update
- Consider undo capability in future (not for MVP)

## Verification
- [ ] Click X - item disappears
- [ ] Restart app - item still gone
- [ ] Works for any item in list
