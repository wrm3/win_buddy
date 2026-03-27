---
id: 204
title: 'Add nested toolbar support'
type: feature
status: pending
priority: medium
phase: 2
subsystems: [ui]
project_context: 'Allow toolbars within toolbars for deeper organization'
dependencies: [201, 202]
---

# Task: Add nested toolbar support

## Objective
Allow toolbars to contain sub-toolbars, creating a hierarchical launcher.

## Acceptance Criteria
- [ ] Toolbar can contain shortcuts OR sub-toolbars
- [ ] Click sub-toolbar expands its contents in new arc
- [ ] Breadcrumb or back navigation to return
- [ ] Reasonable depth limit (2-3 levels)
- [ ] Visual distinction between toolbar and shortcut

## Implementation Notes
- Toolbar item type: "shortcut" or "toolbar"
- Click toolbar: navigate into (expand its items)
- Add "Back" button or click center to go up
- Store hierarchy in JSON: toolbars contain items[]
- Limit max depth to prevent complexity

## Verification
- [ ] Create nested structure
- [ ] Navigate into sub-toolbar
- [ ] Navigate back to parent
- [ ] Deep nesting (3 levels) works
