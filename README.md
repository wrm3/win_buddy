# WinBuddy

A lightweight, always-on-top floating productivity widget for Windows that combines a quick to-do reminder list with an innovative hexagonal radial app launcher.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.10+-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-blue.svg)

## Features

### 📋 Quick To-Do List
- Simple, always-visible reminders
- Add/edit/delete with minimal friction
- Double-click to edit inline
- Persistent storage across restarts

### ⬡ Hexagonal App Launcher
- Modern radial menu design
- Create named toolbars (e.g., "Dev Tools", "Browser", "Games")
- Drag-and-drop shortcuts from Explorer
- Nested toolbar support
- Right-click for toolbar management

### 🎯 Always Accessible
- Stays on top of all windows (like Teams screen share bar)
- Draggable to any position
- Minimizes to system tray
- Auto-start with Windows option
- Position remembered across sessions

## Installation

### Prerequisites
- Python 3.12 or higher
- Windows 10/11 (Linux/Mac support possible with minor adjustments)

### Quick Start

```bash
# Clone or download the project
cd WinBuddy

# Install dependencies with UV
uv sync

# Run the application
uv run python main.py
```

### Running on Startup

1. Right-click the system tray icon
2. Check "Start with Windows"

Or manually via right-click on the title bar.

## Usage

### To-Do List
1. Click the **+** button to add a reminder
2. Type your reminder and press **Enter**
3. Double-click any item to edit
4. Click **×** on an item to delete it

### Hexagonal Launcher
1. Click the center hex to expand toolbars
2. **Right-click** in the expanded area to add a new toolbar
3. **Drag files/folders** from Explorer onto a toolbar to add shortcuts
4. Click a toolbar to see its shortcuts
5. Click a shortcut to launch it
6. **Right-click** a toolbar to rename, change color, or delete

### Window Controls
- **Drag** the title bar to move the widget
- **Click X** or **minimize** to hide to system tray
- **Click tray icon** to restore
- **Right-click tray icon** for menu with Exit option

## File Structure

```
WinBuddy/
├── main.py                 # Application entry point
├── pyproject.toml          # Project configuration
├── src/winbuddy/
│   ├── __init__.py
│   ├── storage.py          # JSON data persistence
│   ├── autostart.py        # Windows registry auto-start
│   └── widgets/
│       ├── __init__.py
│       ├── main_window.py  # Main frameless window
│       ├── todo_list.py    # To-do list widget
│       └── hex_launcher.py # Hexagonal launcher widget
└── README.md
```

## Data Storage

User data is stored in:
- Windows: `%APPDATA%\WinBuddy\`
  - `settings.json` - Window position, preferences
  - `todos.json` - To-do items
  - `launchers.json` - Toolbar and shortcut configuration

## Building an Executable

To create a standalone `.exe`:

```bash
# Install PyInstaller
uv pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name WinBuddy main.py
```

The executable will be in `dist/WinBuddy.exe`.

## Cross-Platform Notes

While designed for Windows, the core functionality uses PyQt6 which is cross-platform:
- **Windows**: Full support including auto-start and system tray
- **Linux**: Works with desktop environment tray support
- **macOS**: Works with menu bar support (may need adjustments)

## License

MIT License - feel free to use, modify, and distribute.

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

---

Made with ❤️ for productivity enthusiasts who miss their quick launch toolbars.
