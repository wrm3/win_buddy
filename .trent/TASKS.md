# WinBuddy — Master Task List

**Project**: WinBuddy — Floating Productivity Widget
**Type**: delivery
**PRD**: `.trent/PRD.md`
**Subsystems**: `.trent/SUBSYSTEMS.md`
**Architecture Constraints**: `.trent/ARCHITECTURE_CONSTRAINTS.md`

---

## Status Indicators
- `[ ]` = Pending (no task file yet) — CODING BLOCKED
- `[📋]` = Task file created, ready to start
- `[📝]` = Spec being written (TTL: 1 hour)
- `[🔄]` = In Progress (claimed by agent, has TTL)
- `[🔍]` = Awaiting Verification (impl done, reviewer pending — different agent required)
- `[⏳]` = Resource-Gated (waiting on GPU/storage/API credits/external service)
- `[✅]` = Completed (verified by different agent)
- `[❌]` = Failed/Cancelled
- `[⏸️]` = Paused
- `[🌾]` = Harvested (done but approach superseded — preserved as reference)

---

## Phase 0: Setup & Infrastructure [✅]

### Subsystem: core
- [✅] **Task 001**: Project setup with UV and PyQt6 — pyproject.toml, venv, main.py entry point
- [✅] **Task 002**: Create main window with frameless, always-on-top behavior — Qt flags set, window renders
- [✅] **Task 003**: Implement draggable window functionality — mouse press/move events wire up drag
- [✅] **Task 004**: Add system tray integration — tray icon, right-click menu, minimize-to-tray
- [✅] **Task 005**: Implement auto-start on Windows boot — Registry key written on first launch
- [✅] **Task 006**: Create JSON storage manager — read/write JSON in %APPDATA%/WinBuddy/

---

## Phase 1: To-Do Widget [✅]

### Subsystem: todo-widget
- [✅] **Task 100**: Create to-do list UI component — QListWidget with styled items
- [✅] **Task 101**: Implement add todo functionality — + button opens inline editor, Enter saves
- [✅] **Task 102**: Implement edit todo functionality — double-click edits inline
- [✅] **Task 103**: Implement delete todo functionality — right-click or Delete key removes item
- [✅] **Task 104**: Connect todo list to storage persistence — todos saved/loaded via storage manager

---

## Phase 2: Hexagonal Launcher [✅]

### Subsystem: hex-launcher
- [✅] **Task 200**: Design and create central hex button — custom QPainter hexagon, hover glow
- [✅] **Task 201**: Implement radial expansion animation — toolbar buttons animate outward on hover
- [✅] **Task 202**: Create toolbar management (add/rename/delete) — right-click context menu
- [✅] **Task 203**: Implement shortcut drag-and-drop — Explorer files drag onto toolbar slots
- [✅] **Task 204**: Add nested toolbar support — toolbars can contain sub-toolbars
- [✅] **Task 205**: Connect launcher to storage persistence — toolbars/shortcuts saved via storage manager

---

## Bugs
*(See `.trent/BUGS.md` for full bug list)*

---

## Completed Tasks
All Phase 0, Phase 1, and Phase 2 tasks completed on 2026-02-03.

---

## Harvested Tasks
*(Tasks that were completed but whose approach was superseded — preserved for reference)*

---

**Last Updated**: 2026-03-27
**Phase 0 Progress**: 6/6 tasks ✅
**Phase 1 Progress**: 5/5 tasks ✅
**Phase 2 Progress**: 6/6 tasks ✅
**Overall Progress**: 17/17 tasks complete
