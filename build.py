"""Build WinBuddy into a distributable .exe using PyInstaller.

Usage:
    uv run python build.py
    
Output:
    dist/WinBuddy/WinBuddy.exe  (folder mode - smaller, faster build)
    dist/WinBuddy.exe            (onefile mode - single exe, easier to share)
"""

import subprocess
import sys


def build():
    """Run PyInstaller to create the executable."""
    args = [
        sys.executable, "-m", "PyInstaller",
        "--name", "WinBuddy",
        # Single file exe - easiest to share
        "--onefile",
        # Windowed mode (no console window)
        "--windowed",
        # Hidden imports that PyInstaller may miss
        "--hidden-import", "src.winbuddy",
        "--hidden-import", "src.winbuddy.widgets",
        "--hidden-import", "src.winbuddy.widgets.main_window",
        "--hidden-import", "src.winbuddy.widgets.hex_launcher",
        "--hidden-import", "src.winbuddy.widgets.todo_list",
        "--hidden-import", "src.winbuddy.storage",
        "--hidden-import", "src.winbuddy.autostart",
        "--hidden-import", "src.winbuddy.icons",
        # Add the src directory as a data/path so imports work
        "--add-data", "src;src",
        # Clean build
        "--clean",
        # Overwrite previous build
        "--noconfirm",
        # Entry point
        "main.py",
    ]

    print("=" * 60)
    print("  Building WinBuddy.exe")
    print("=" * 60)
    print()
    print(f"Running: {' '.join(args)}")
    print()

    result = subprocess.run(args, cwd="g:\\WinBuddy")

    if result.returncode == 0:
        print()
        print("=" * 60)
        print("  BUILD SUCCESSFUL!")
        print("=" * 60)
        print()
        print("  Output: dist\\WinBuddy.exe")
        print()
        print("  To share with coworkers:")
        print("  1. Copy dist\\WinBuddy.exe to them")
        print("  2. They double-click it to run")
        print("  3. That's it! No Python install needed.")
        print()
        print("  Note: Windows SmartScreen may warn on first run")
        print("  since the exe isn't code-signed. They just click")
        print("  'More info' -> 'Run anyway'.")
        print("=" * 60)
    else:
        print()
        print("BUILD FAILED - check output above for errors")
        sys.exit(1)


if __name__ == "__main__":
    build()
