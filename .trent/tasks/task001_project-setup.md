---
id: 1
title: 'Project setup with UV and PyQt6'
type: feature
status: pending
priority: critical
phase: 0
subsystems: [core]
project_context: 'Initialize Python project with UV package manager and PyQt6 dependencies'
dependencies: []
---

# Task: Project setup with UV and PyQt6

## Objective
Create the project structure with UV as package manager and install PyQt6 for cross-platform GUI development.

## Acceptance Criteria
- [ ] pyproject.toml created with project metadata
- [ ] PyQt6 added as dependency
- [ ] Virtual environment created via UV
- [ ] main.py entry point created
- [ ] Basic "Hello World" window launches

## Implementation Notes
- Use `uv init` to create project
- Add PyQt6 >= 6.6.0
- Create src/winbuddy/ package structure
- Entry point in main.py at root

## Verification
- [ ] `uv run python main.py` launches window
- [ ] No import errors
