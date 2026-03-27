---
id: 5
title: 'Implement auto-start on Windows boot'
type: feature
status: pending
priority: medium
phase: 0
subsystems: [system-integration]
project_context: 'Enable the app to start automatically when Windows boots'
dependencies: [4]
---

# Task: Implement auto-start on Windows boot

## Objective
Add the application to Windows startup so it launches automatically on boot.

## Acceptance Criteria
- [ ] Option in settings/tray menu to enable/disable auto-start
- [ ] When enabled, app starts on Windows login
- [ ] Uses Windows Registry Run key
- [ ] Works with both script and packaged exe

## Implementation Notes
- Use winreg module to access registry
- Add entry to HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
- Store path to main.py or .exe
- For dev: use pythonw to avoid console window
- Provide toggle in right-click tray menu

## Verification
- [ ] Enable auto-start via menu
- [ ] Reboot Windows
- [ ] App appears automatically
- [ ] Disable and verify it doesn't start
