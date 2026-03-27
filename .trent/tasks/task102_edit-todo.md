---
id: 102
title: 'Implement edit todo functionality'
type: feature
status: pending
priority: high
phase: 1
subsystems: [ui]
project_context: 'Allow editing existing todo items'
dependencies: [100]
---

# Task: Implement edit todo functionality

## Objective
Allow users to edit existing todo items by double-clicking.

## Acceptance Criteria
- [ ] Double-click todo opens inline edit
- [ ] Current text pre-filled in input
- [ ] Enter saves changes
- [ ] Escape cancels edit
- [ ] Changes persist immediately

## Implementation Notes
- On double-click, replace label with QLineEdit
- Pre-fill with current text
- On Enter, update model and replace back to label
- On Escape or focus out, restore original
- Emit signal for storage to save

## Verification
- [ ] Double-click - edit mode starts
- [ ] Original text shown
- [ ] Edit and Enter - text updated
- [ ] Escape - original text restored
