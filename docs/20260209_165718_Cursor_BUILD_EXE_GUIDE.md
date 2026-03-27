# Building WinBuddy.exe
 
How to compile WinBuddy into a standalone `.exe` that anyone can run without installing Python.

## Prerequisites

- Python 3.12+ installed
- [UV](https://docs.astral.sh/uv/) package manager installed
- WinBuddy source code

## Build Steps

1. Open a terminal (PowerShell or Command Prompt)

2. Navigate to the WinBuddy project folder:
   ```powershell
   cd g:\WinBuddy
   ```

3. Run the build script:
   ```powershell
   uv run python build.py
   ```

4. Wait for the build to complete (~1-2 minutes). You'll see:
   ```
   ============================================================
     BUILD SUCCESSFUL!
   ============================================================
   ```

5. The output file is at:
   ```
   g:\WinBuddy\dist\WinBuddy.exe
   ```

## Output Details

- **File**: `dist\WinBuddy.exe`
- **Size**: ~38 MB (includes Python runtime, PyQt6, and all dependencies)
- **Self-contained**: No Python or other software installation required on target machine

## Sharing with Others

1. Copy `dist\WinBuddy.exe` to your coworkers (email, Teams, shared drive, USB, etc.)
2. They double-click it to run
3. That's it!

### First-Run SmartScreen Warning

Since the `.exe` is not code-signed, Windows SmartScreen will show a warning the first time it's run:

1. Click **"More info"**
2. Click **"Run anyway"**

This only happens once per machine.

## User Data Location

Each person's data is stored independently in their own:
```
%APPDATA%\WinBuddy\
```

This includes:
- `todos.json` - Reminder items and colors
- `launchers.json` - Quick Launch toolbar groups and shortcuts
- `settings.json` - Window positions, sizes, preferences

## Rebuilding After Code Changes

After making changes to the source code, just run the build script again:

```powershell
cd g:\WinBuddy
uv run python build.py
```

The previous build will be overwritten automatically.

## Troubleshooting

### Build fails with missing module
Make sure all dependencies are installed:
```powershell
uv sync
```

### Exe won't start / crashes immediately
Run from command line to see error output:
```powershell
.\dist\WinBuddy.exe
```

### Antivirus flags the exe
PyInstaller-built executables are sometimes flagged as false positives. You may need to add an exclusion in your antivirus software for the `dist\` folder or the exe file.
