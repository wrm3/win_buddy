---
id: 202
title: 'Create toolbar management (add/rename/delete)'
type: feature
status: pending
priority: high
phase: 2
subsystems: [ui]
project_context: 'Allow users to create and organize their toolbars'
dependencies: [200, 201]
---

# Task: Create toolbar management (add/rename/delete)

## Objective
Allow users to add new toolbars, rename existing ones, and delete unwanted ones.

## Acceptance Criteria
- [ ] Right-click on expanded area shows "Add Toolbar" option
- [ ] Right-click on toolbar button shows "Rename" and "Delete"
- [ ] Add opens dialog for toolbar name
- [ ] Rename opens dialog with current name
- [ ] Delete confirms before removing
- [ ] Changes persist to storage

## Implementation Notes
- Use QMenu for context menus
- QInputDialog for name input
- QMessageBox for delete confirmation
- Each toolbar has: id, name, color (optional), shortcuts[]
- Maximum ~8 toolbars for first ring

## Verification
- [ ] Right-click hex - can add toolbar
- [ ] Right-click toolbar - can rename/delete
- [ ] New toolbar appears after adding
- [ ] Changes survive restart
