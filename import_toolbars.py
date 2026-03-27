"""Import existing Windows toolbars into WinBuddy.

This script reads shortcuts from a folder structure and imports them
into WinBuddy's launcher configuration.

Usage:
    uv run python import_toolbars.py [path_to_toolbars]
    
Default path: C:\\Users\\wrm3\\Toolbars
"""

import json
import os
import sys
import uuid
from pathlib import Path

# Colors for toolbars
TOOLBAR_COLORS = [
    "#3498db",  # Blue
    "#e74c3c",  # Red
    "#2ecc71",  # Green
    "#f39c12",  # Orange
    "#9b59b6",  # Purple
    "#1abc9c",  # Teal
    "#e91e63",  # Pink
    "#607d8b",  # Gray
]


def get_winbuddy_data_dir():
    """Get WinBuddy data directory."""
    if os.name == 'nt':
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:
        base = os.path.expanduser('~/.config')
    return Path(base) / 'WinBuddy'


def load_launchers(data_dir: Path) -> dict:
    """Load existing launcher configuration."""
    launcher_file = data_dir / 'launchers.json'
    if launcher_file.exists():
        with open(launcher_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'toolbars': [], 'current_toolbar': None}


def save_launchers(data_dir: Path, launchers: dict):
    """Save launcher configuration."""
    launcher_file = data_dir / 'launchers.json'
    data_dir.mkdir(parents=True, exist_ok=True)
    with open(launcher_file, 'w', encoding='utf-8') as f:
        json.dump(launchers, f, indent=2, ensure_ascii=False)


def import_toolbars(source_path: Path, replace: bool = False):
    """Import toolbars from source path into WinBuddy."""
    data_dir = get_winbuddy_data_dir()
    
    if replace:
        launchers = {'toolbars': [], 'current_toolbar': None}
    else:
        launchers = load_launchers(data_dir)
    
    # Get existing toolbar names to avoid duplicates
    existing_names = {tb['name'].lower() for tb in launchers['toolbars']}
    
    # Scan source directory for toolbar folders
    if not source_path.exists():
        print(f"Error: Path not found: {source_path}")
        return False
    
    color_index = len(launchers['toolbars'])
    imported_toolbars = 0
    imported_shortcuts = 0
    
    for folder in sorted(source_path.iterdir()):
        if not folder.is_dir():
            continue
        
        toolbar_name = folder.name
        
        # Skip if already exists
        if toolbar_name.lower() in existing_names:
            print(f"  Skipping '{toolbar_name}' (already exists)")
            continue
        
        # Create toolbar
        toolbar = {
            'id': str(uuid.uuid4()),
            'name': toolbar_name,
            'color': TOOLBAR_COLORS[color_index % len(TOOLBAR_COLORS)],
            'items': [],
        }
        color_index += 1
        
        # Scan for shortcuts
        for shortcut_file in sorted(folder.iterdir()):
            if shortcut_file.is_file():
                # Get name without extension
                name = shortcut_file.stem
                # Clean up common patterns
                name = name.replace(' - Shortcut', '').replace('.exe', '')
                
                shortcut = {
                    'id': str(uuid.uuid4()),
                    'type': 'shortcut',
                    'name': name,
                    'path': str(shortcut_file),
                    'icon_path': None,
                }
                toolbar['items'].append(shortcut)
                imported_shortcuts += 1
        
        if toolbar['items']:
            launchers['toolbars'].append(toolbar)
            imported_toolbars += 1
            print(f"  Imported '{toolbar_name}' with {len(toolbar['items'])} shortcuts")
    
    # Save
    save_launchers(data_dir, launchers)
    
    print(f"\nDone! Imported {imported_toolbars} toolbars with {imported_shortcuts} shortcuts.")
    print(f"Data saved to: {data_dir / 'launchers.json'}")
    print("\nRestart WinBuddy to see the changes.")
    return True


def main():
    # Default path
    default_path = Path(r"C:\Users\wrm3\Toolbars")
    
    # Check for --replace flag
    replace = '--replace' in sys.argv
    
    # Get path from args (skip flags)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    source_path = Path(args[0]) if args else default_path
    
    print(f"Importing toolbars from: {source_path}")
    print("-" * 50)
    
    if replace:
        print("Mode: REPLACE existing toolbars")
    else:
        print("Mode: ADD to existing toolbars (use --replace to overwrite)")
    
    print()
    import_toolbars(source_path, replace)


if __name__ == "__main__":
    main()
