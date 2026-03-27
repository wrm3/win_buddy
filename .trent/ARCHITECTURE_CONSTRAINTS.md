# ARCHITECTURE_CONSTRAINTS.md

## Purpose

This file is loaded at every session start. Constraints listed here are
**non-negotiable** — they govern decisions made throughout the project.

No AI agent may override, work around, or silently ignore a constraint. Constraints
may only be changed or removed with **explicit user approval** as described below.

---

## Change Authority

### Who can change constraints

The user has ultimate authority over all constraints. AI agents may:
- Suggest adding, modifying, or removing a constraint
- Explain the tradeoffs of a proposed change
- Flag when a requested action conflicts with an active constraint

AI agents may NOT:
- Assume silence or inferred agreement is approval
- Modify a constraint based on conversational context alone
- Bypass a constraint temporarily without explicit approval

### What counts as approval

Approval requires an explicit, unambiguous statement from the user in the
current session. Accepted approval phrases include:
  - "yes", "approved", "accept", "go ahead", "confirmed", "do it"
  - Any phrase that clearly authorizes the specific change being proposed

### Logging requirement

Every change to this file must be recorded in the Change Log at the bottom
of this document. The log is append-only. Entries are never removed.

---

## Active Constraints

### C-001: Python + PyQt6 Only — No Additional UI Frameworks

**Non-negotiable**: yes

**Rationale**: WinBuddy is built on Python 3.11+ and PyQt6 to maintain cross-platform
potential. Adding additional UI frameworks (Tkinter, wxPython, web views) would
fragment the codebase and break the single-framework architecture.

**Applies to**: all UI components and window management code

**What this means in practice**:
- All GUI elements must use PyQt6 widgets or custom PyQt6 painting
- No embedded web views (QWebEngineView) unless explicitly approved
- No mixing of Qt5 and Qt6 APIs

**Violation examples**:
- Installing tkinter or wxPython as a fallback
- Using a web-based UI framework inside a QWebEngineView without approval

**Change authority**: User. May be revisited if a specific feature requires web rendering.

---

### C-002: Local File Storage Only — No Network Calls

**Non-negotiable**: yes

**Rationale**: WinBuddy is a personal privacy-focused tool. All data must stay
on the local machine. No telemetry, no cloud sync, no external API calls.

**Applies to**: all data persistence and network code

**What this means in practice**:
- All data stored in JSON files under `%APPDATA%/WinBuddy/`
- No HTTP requests at runtime (except explicit future feature approval)
- No analytics or crash reporting without explicit user consent

**Violation examples**:
- Adding requests/httpx to pyproject.toml without approval
- Sending any data to external servers

**Change authority**: User. May be revisited if cloud sync is added as an explicit feature.

---

### C-003: UV for Package Management — No pip Direct

**Non-negotiable**: yes

**Rationale**: This project uses UV for reproducible environment management.
Direct pip calls bypass the lock file and can introduce version drift.

**Applies to**: all dependency installation and environment management

**What this means in practice**:
- Use `uv add` to add dependencies (updates pyproject.toml + lock file)
- Use `uv run` to run scripts in the managed environment
- Never run `pip install` directly in the project environment

**Violation examples**:
- `pip install some-package` instead of `uv add some-package`
- Manually editing pyproject.toml without running `uv sync` afterward

**Change authority**: User.

---

### C-004: No Breaking Changes to Storage Schema Without Migration

**Non-negotiable**: yes

**Rationale**: User data (todos, shortcuts, settings) is stored in JSON. Changing
field names or structure without a migration will silently corrupt existing data.

**Applies to**: `src/winbuddy/storage_manager.py` and any JSON schema changes

**What this means in practice**:
- Any new field must have a default value for backward compatibility
- Removing or renaming a field requires a migration function in the storage manager
- Version field in JSON must be incremented on schema changes

**Violation examples**:
- Renaming `"toolbar_name"` to `"name"` without updating existing JSON files
- Removing a field that existing saves rely on

**Change authority**: User. Required before any storage schema modification.

---

## Change Log

All changes to constraints are recorded here. This table is append-only.

| Date       | Constraint | Change                                  | Approved By      |
|------------|------------|-----------------------------------------|------------------|
| 2026-03-27 | C-001      | Initial constraint added                | trent v6 migration |
| 2026-03-27 | C-002      | Initial constraint added                | trent v6 migration |
| 2026-03-27 | C-003      | Initial constraint added                | trent v6 migration |
| 2026-03-27 | C-004      | Initial constraint added                | trent v6 migration |

---

## Session Start Summary

At the start of every session, the AI must display a compact summary of all
active constraints:

```
ACTIVE CONSTRAINTS:
  C-001: Python + PyQt6 Only — no other UI frameworks without approval
  C-002: Local File Storage Only — no network calls at runtime
  C-003: UV for Package Management — no direct pip install
  C-004: No breaking storage schema changes without migration
Full constraints: .trent/ARCHITECTURE_CONSTRAINTS.md
```
