---
phase: 0
name: 'Setup & Infrastructure'
status: completed
subsystems: [core, storage, system-integration]
task_range: '1-99'
prerequisites: []
started_date: '2026-02-03'
completed_date: '2026-02-03'
pivoted_from: null
pivot_reason: ''
---

# Phase 0: Setup & Infrastructure

## Overview
Set up the project foundation including Python environment, PyQt6 framework, core window behavior, system tray integration, and auto-start capability.

## Objectives
- Create project structure with UV package manager
- Establish PyQt6 as UI framework
- Build frameless, always-on-top main window
- Implement draggable window behavior
- Add system tray with context menu
- Enable Windows auto-start via registry
- Create JSON storage manager for persistence

## Deliverables
- [ ] pyproject.toml with dependencies
- [ ] Main application entry point
- [ ] Draggable, frameless main window
- [ ] System tray icon with menu
- [ ] Auto-start registry entry
- [ ] Storage manager class

## Acceptance Criteria
- [ ] App launches with `uv run python main.py`
- [ ] Window stays on top of other apps
- [ ] Window can be dragged anywhere
- [ ] Close minimizes to tray
- [ ] Right-click tray shows Exit option
- [ ] Data persists in JSON files

## Notes
Using PyQt6 for cross-platform potential. Focus on Windows first, Mac/Linux adjustments later.
