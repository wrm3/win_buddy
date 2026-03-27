# PRD: WinBuddy

## 1. Product overview

### 1.1 Document title and version
- PRD: WinBuddy - Floating Productivity Widget
- Version: 1.0

### 1.2 Product summary
WinBuddy is a lightweight, always-on-top floating widget for Windows that combines two essential productivity features: a quick to-do reminder list and an innovative hexagonal radial app launcher.

The to-do component provides a simple, always-visible list of short reminders to help maintain focus throughout the workday. Unlike complex task management tools, it focuses on quick capture and visibility - just short names to jog memory.

The hexagonal launcher brings back the beloved quick-launch toolbar experience from older Windows versions, reimagined as a modern radial menu. Users can organize shortcuts into named "toolbars" that expand from a central hex, with support for nested sub-toolbars. This creates a compact yet powerful app launching system that stays out of the way until needed.

## 2. Goals

### 2.1 Business goals
- Provide a free, open-source productivity tool
- Demonstrate modern Python desktop development
- Create a cross-platform foundation for future expansion

### 2.2 User goals
- Quick access to frequently used applications
- Always-visible task reminders without screen clutter
- Restore quick-launch functionality lost in newer Windows versions
- Minimal cognitive load for daily use

### 2.3 Non-goals
- Replace full-featured task management tools (Todoist, Notion, etc.)
- Compete with Windows Start Menu or Taskbar
- Provide cloud sync or collaboration features
- Support themes or extensive customization
- Plugin or extension system

## 3. User personas

### 3.1 Key user types
- Power users who miss Windows XP/7 quick launch toolbars
- Knowledge workers needing constant task reminders
- Developers and IT professionals with many tools

### 3.2 Basic persona details
- **Power User Pat**: Uses 20+ applications daily, wants one-click access to favorites organized by workflow
- **Focused Developer Dana**: Needs visible reminders of current sprint tasks while coding
- **Multitasker Morgan**: Switches contexts frequently, needs quick orientation on current priorities

### 3.3 Role-based access
- **Single User**: Full access to all features (no multi-user support)

## 4. Phases

### 4.1 Phase Overview

- **Phase 0: Setup & Infrastructure** (Task IDs: 1-99)
  - Project setup, dependencies, core window framework
  - Draggable, always-on-top behavior
  - System tray integration
  - Status: [ ] Pending

- **Phase 1: To-Do Widget** (Task IDs: 100-199)
  - To-do list UI component
  - Add/edit/delete functionality
  - Persistent storage
  - Status: [ ] Pending

- **Phase 2: Hexagonal Launcher** (Task IDs: 200-299)
  - Central hex button design
  - Radial expansion animation
  - Toolbar management (add/rename/delete)
  - Shortcut dropping and management
  - Nested toolbar support
  - Status: [ ] Pending

### 4.2 Phase References
- Phase documents: `.trent/phases/`
- Phase template: `.trent/templates/phase_template.md`

## 5. User experience

### 5.1 Entry points & first-time user flow
**First Launch:**
1. Widget appears in screen center
2. Empty to-do list with "Click + to add" hint
3. Hex launcher button visible below todos
4. Brief tooltip explaining drag-to-move

### 5.2 Core experience
**Adding a To-Do:**
1. Click + button or press keyboard shortcut
2. Type short reminder text
3. Press Enter to save
4. Item appears in list immediately

**Launching an App:**
1. Hover over central hex
2. Toolbar buttons expand in arc/ring
3. Click toolbar to show its shortcuts
4. Click shortcut to launch

**Adding a Shortcut:**
1. Drag file/folder/URL onto a toolbar
2. Shortcut appears in that toolbar
3. Right-click to rename or remove

### 5.3 Advanced features & edge cases
- Drag widget to any screen edge or position
- Double-click todo to edit inline
- Right-click widget for settings/exit menu
- Click X or minimize button to send to tray
- Click tray icon to restore

### 5.4 UI/UX highlights
- Semi-transparent background to reduce visual weight
- Smooth animations for hex expansion
- Color-coded toolbars for quick identification
- Compact vertical layout (todo list above, hex below)

## 6. Narrative
Sarah starts her day by glancing at WinBuddy floating in the corner of her screen. Three items remind her: "Review PR #234", "Call vendor", "Submit timesheet". She drags the widget to her second monitor and hovers over the hex launcher. The "Dev Tools" toolbar expands, and with one click she opens VS Code. Later, she right-clicks a todo and marks it done. At lunch, she clicks the X to minimize to tray. After lunch, one click on the tray icon and WinBuddy is back, keeping her focused all afternoon.

## 7. Success metrics

### 7.1 User-centric metrics
- Time to add todo: < 3 seconds
- Time to launch app: < 2 clicks
- Widget positioning: Remember across sessions

### 7.2 Business metrics
- N/A (personal tool)

### 7.3 Technical metrics
- Startup time: < 2 seconds
- Memory usage: < 50 MB idle
- CPU usage: < 1% idle

## 8. Technical considerations

### 8.1 Affected subsystems
- **Primary subsystems**:
  - UI Layer: Main window, todo list, hex launcher
  - Storage Layer: JSON persistence
  - System Integration: Tray, auto-start, shortcuts

### 8.2 Integration points
- Windows System Tray (QSystemTrayIcon)
- Windows Registry (auto-start via winreg)
- Shell shortcuts (.lnk files via win32com or pywin32)
- Drag-and-drop from Explorer

### 8.3 Data storage & privacy
- Local JSON files only
- User data in `%APPDATA%/WinBuddy/`
- No telemetry or network calls
- No sensitive data stored

### 8.4 Scalability & performance
- Single-user, single-machine
- Performance targets easily achievable
- No database needed

### 8.5 Potential challenges
- **Custom hex layout**: Requires manual positioning math
- **Always-on-top conflicts**: Some apps fight for topmost
- **Drag-drop shortcuts**: Reading .lnk files needs pywin32
- **Cross-platform**: Mac/Linux will need platform-specific adjustments

## 9. Milestones & sequencing

### 9.1 Project estimate
- **Size: Small**: 1-2 days for MVP

### 9.2 Team size & composition
- Solo developer with AI assistance

### 9.3 Suggested phases

- **Phase 0: Setup** (Tasks 1-99)
  - Key deliverables: Running window, tray icon, auto-start

- **Phase 1: To-Do Widget** (Tasks 100-199)
  - Key deliverables: Add/edit/delete todos, persistence

- **Phase 2: Hex Launcher** (Tasks 200-299)
  - Key deliverables: Radial menu, toolbars, shortcuts

## 10. User stories

### 10.1 Always-Visible Widget
- **ID**: US-001
- **Description**: As a user, I want the widget to stay on top of other windows, so I can always see my reminders.
- **Acceptance Criteria**:
  - Widget remains visible over other applications
  - Widget can be dragged to any position
  - Position is remembered after restart

### 10.2 Quick To-Do Entry
- **ID**: US-002
- **Description**: As a user, I want to quickly add a reminder, so I don't lose my thought.
- **Acceptance Criteria**:
  - One-click to open add dialog
  - Enter to save
  - Immediate display in list

### 10.3 Radial App Launcher
- **ID**: US-003
- **Description**: As a user, I want to organize my apps in a radial menu, so I can launch them with minimal clicks.
- **Acceptance Criteria**:
  - Hover to expand toolbars
  - Click to expand toolbar contents
  - One-click to launch shortcut

### 10.4 System Tray Integration
- **ID**: US-004
- **Description**: As a user, I want the widget to minimize to the system tray, so it's not in my way when I don't need it.
- **Acceptance Criteria**:
  - Close button minimizes to tray (not exits)
  - Right-click tray for menu with Exit option
  - Click tray icon to restore

### 10.5 Persistent Data
- **ID**: US-005
- **Description**: As a user, I want my todos and shortcuts saved, so I don't lose them after restart.
- **Acceptance Criteria**:
  - Todos persist across app restarts
  - Shortcuts persist across app restarts
  - Widget position persists across restarts
