---
id: 203
title: 'Implement shortcut drag-and-drop'
type: feature
status: pending
priority: high
phase: 2
subsystems: [ui, system-integration]
project_context: 'Add shortcuts by dragging from Explorer'
dependencies: [202]
---

# Task: Implement shortcut drag-and-drop

## Objective
Allow users to drag files, folders, or shortcuts from Explorer onto a toolbar to add them.

## Acceptance Criteria
- [ ] Drag file/folder onto expanded toolbar adds shortcut
- [ ] Drag .lnk file works (Windows shortcuts)
- [ ] Drag .url file works (web shortcuts)
- [ ] Shortcut shows icon and name
- [ ] Click shortcut launches the target

## Implementation Notes
- Enable setAcceptDrops(True) on toolbar
- Handle dragEnterEvent and dropEvent
- Extract file path from QMimeData
- For .lnk files, may need pywin32 to read target
- Store: {name, path, icon_path (optional)}
- Use QProcess or os.startfile to launch

## Verification
- [ ] Drag .exe onto toolbar - shortcut added
- [ ] Drag folder - opens in Explorer
- [ ] Drag .lnk - launches target app
- [ ] Drag URL - opens in browser
