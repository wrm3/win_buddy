# Subsystems Registry — WinBuddy

## Overview
This document tracks all subsystems/components in the WinBuddy project.

---

## Subsystems

### core
- **Purpose**: Main application window, always-on-top frameless widget, system tray integration, auto-start
- **Location**: `src/winbuddy/main_window.py`, `src/winbuddy/system_tray.py`, `src/winbuddy/auto_start.py`
- **Dependencies**: PyQt6, winreg (Windows Registry)
- **Dependents**: todo-widget, hex-launcher, storage

### todo-widget
- **Purpose**: To-do list UI — add, edit, delete short reminder items
- **Location**: `src/winbuddy/todo_widget.py`
- **Dependencies**: core, storage
- **Dependents**: *(none)*

### hex-launcher
- **Purpose**: Hexagonal radial app launcher — toolbars, shortcuts, nested sub-toolbars
- **Location**: `src/winbuddy/hex_launcher.py`, `src/winbuddy/toolbar_widget.py`
- **Dependencies**: core, storage
- **Dependents**: *(none)*

### storage
- **Purpose**: JSON persistence layer — read/write todos, shortcuts, settings to %APPDATA%/WinBuddy/
- **Location**: `src/winbuddy/storage_manager.py`
- **Dependencies**: *(none — pure stdlib)*
- **Dependents**: todo-widget, hex-launcher, core

---

## Subsystem Relationships

```
  [core]
    |
    +---> [todo-widget] ---> [storage]
    |
    +---> [hex-launcher] --> [storage]
```

---

**Last Updated**: 2026-03-27
