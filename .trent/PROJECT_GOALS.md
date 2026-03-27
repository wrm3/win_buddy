# PROJECT_GOALS.md

> **Strategic north star for WinBuddy.**
> The AI loads this at session start to validate decisions and steer work toward what matters.

---

## Vision

A lightweight, always-on-top floating productivity widget for Windows that combines a quick to-do reminder list with a hexagonal radial app launcher — restoring the quick-launch experience of older Windows with a modern, elegant design.

---

## Primary Goals

| ID   | Goal                              | Target / Metric                              | Status   |
|------|-----------------------------------|----------------------------------------------|----------|
| G-01 | Always-visible productivity widget | Widget stays on top, survives app switches    | complete |
| G-02 | Quick app launching               | App launched in < 2 clicks from hex launcher  | complete |
| G-03 | Persistent state                  | Todos and shortcuts survive restarts          | complete |
| G-04 | Windows system integration        | System tray, auto-start, file shortcuts work  | complete |

---

## Secondary Goals

Goals that support the primaries but aren't critical path:

- **Minimal footprint**: Startup < 2s, memory < 50MB, CPU < 1% idle
- **Zero-documentation UX**: No manual required to operate the widget
- **Cross-platform foundation**: PyQt6 base enables future Linux/Mac ports
- **Distributable executable**: PyInstaller packaging for .exe distribution

---

## Non-Goals (Explicitly Out of Scope)

Things we are consciously NOT building in this project:

- Cloud sync or multi-device support — local-only is intentional
- Multi-user support or authentication — personal tool only
- Complex task management (due dates, priorities, categories) — keep it simple
- Plugin/extension system — no extensibility required for v1
- Themes beyond basic dark/light — cosmetic scope creep
- Mobile companion app — Windows desktop only

---

## Success Metrics

How we know we've achieved the vision:

- Time to add a todo: < 3 seconds
- Time to launch an app: < 2 clicks from the hex button
- Widget position remembered across restarts: ✅
- Memory usage at idle: < 50MB
- CPU usage at idle: < 1%

---

## Goal Log

| Date       | Change                                      | Reason               |
|------------|---------------------------------------------|----------------------|
| 2026-02-03 | Initial goals defined — MVP completed       | Project setup        |
| 2026-03-27 | Goals documented in PROJECT_GOALS.md        | trent v6 migration   |

---

## Goal Status Reference

| Status    | Meaning                                      |
|-----------|----------------------------------------------|
| `active`  | Current active goal being worked toward      |
| `complete`| Goal achieved — log the completion date      |
| `retired` | Goal no longer relevant — log the reason     |
| `paused`  | Temporarily deprioritized                    |
