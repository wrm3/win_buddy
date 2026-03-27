---
id: 100
title: 'Create to-do list UI component'
type: feature
status: pending
priority: critical
phase: 1
subsystems: [ui]
project_context: 'Build the visual component for displaying todo items'
dependencies: [2]
---

# Task: Create to-do list UI component

## Objective
Create a clean, minimal list widget to display todo items in the main window.

## Acceptance Criteria
- [ ] Vertical list of todo items
- [ ] Each item shows text and delete button
- [ ] Add button at bottom of list
- [ ] Scrollable if many items
- [ ] Clean, modern styling

## Implementation Notes
- Use QListWidget or custom QVBoxLayout with item widgets
- Custom TodoItem widget with text label and delete button
- Add button fixed at bottom
- Apply stylesheet for modern look
- Limit visible items, scroll for overflow

## Verification
- [ ] Empty list shows placeholder text
- [ ] Items display correctly
- [ ] Scroll works with many items
- [ ] Looks clean and professional
