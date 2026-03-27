---
id: 101
title: 'Implement add todo functionality'
type: feature
status: pending
priority: critical
phase: 1
subsystems: [ui]
project_context: 'Quick add capability for new todos'
dependencies: [100]
---

# Task: Implement add todo functionality

## Objective
Allow users to quickly add a new todo item with minimal friction.

## Acceptance Criteria
- [ ] Click + button opens inline input field
- [ ] Type text and press Enter to save
- [ ] Escape cancels without saving
- [ ] New item appears immediately in list
- [ ] Input field clears after adding

## Implementation Notes
- Show QLineEdit when + clicked
- Connect returnPressed signal to add logic
- Focus input automatically
- Hide input after adding
- Generate unique ID for each todo

## Verification
- [ ] Click + - input appears
- [ ] Type and Enter - item added
- [ ] Press Escape - input closes without adding
- [ ] Can add multiple items quickly
