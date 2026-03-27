"""Storage manager for WinBuddy - handles all data persistence."""

import json
import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class StorageManager:
    """Manages JSON-based storage for todos, launchers, and settings."""

    def __init__(self):
        """Initialize storage manager with appropriate data directory."""
        # Use APPDATA on Windows, fallback for cross-platform
        if os.name == 'nt':
            base = os.environ.get('APPDATA', os.path.expanduser('~'))
        else:
            base = os.path.expanduser('~/.config')
        
        self.data_dir = Path(base) / 'WinBuddy'
        self._ensure_data_dir()
        
        # File paths
        self.settings_file = self.data_dir / 'settings.json'
        self.todos_file = self.data_dir / 'todos.json'
        self.launchers_file = self.data_dir / 'launchers.json'
        
        logger.info(f"Storage initialized at: {self.data_dir}")

    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _load_json(self, filepath: Path, default: Any) -> Any:
        """Load JSON file, returning default if file doesn't exist or is invalid."""
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading {filepath}: {e}. Using default.")
        return default

    def _save_json(self, filepath: Path, data: Any):
        """Save data to JSON file atomically."""
        temp_file = filepath.with_suffix('.tmp')
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            temp_file.replace(filepath)
        except IOError as e:
            logger.error(f"Error saving {filepath}: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise

    # === Settings ===
    
    def load_settings(self) -> dict:
        """Load application settings."""
        default = {
            'window_x': 100,
            'window_y': 100,
            'auto_start': False,
            'opacity': 0.95,
        }
        return self._load_json(self.settings_file, default)

    def save_settings(self, settings: dict):
        """Save application settings."""
        self._save_json(self.settings_file, settings)

    # === Todos ===
    
    def load_todos(self) -> list:
        """Load todo items."""
        return self._load_json(self.todos_file, [])

    def save_todos(self, todos: list):
        """Save todo items."""
        self._save_json(self.todos_file, todos)

    def add_todo(self, text: str) -> dict:
        """Add a new todo item and return it (inserted at the top)."""
        todos = self.load_todos()
        todo = {
            'id': str(uuid.uuid4()),
            'text': text,
            'created_at': datetime.now().isoformat(),
            'completed': False,
        }
        todos.insert(0, todo)
        self.save_todos(todos)
        return todo

    def update_todo(self, todo_id: str, text: str) -> bool:
        """Update a todo item's text."""
        todos = self.load_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                todo['text'] = text
                self.save_todos(todos)
                return True
        return False

    def update_todo_color(self, todo_id: str, color: str) -> bool:
        """Update a todo item's color indicator."""
        todos = self.load_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                todo['color'] = color
                self.save_todos(todos)
                return True
        return False

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item."""
        todos = self.load_todos()
        original_len = len(todos)
        todos = [t for t in todos if t['id'] != todo_id]
        if len(todos) < original_len:
            self.save_todos(todos)
            return True
        return False

    def toggle_todo(self, todo_id: str) -> bool:
        """Toggle a todo item's completed status."""
        todos = self.load_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                todo['completed'] = not todo.get('completed', False)
                self.save_todos(todos)
                return True
        return False

    def reorder_todos(self, todo_ids: list) -> bool:
        """Reorder todos based on the provided list of IDs."""
        todos = self.load_todos()
        # Create a map of id -> todo
        todo_map = {t['id']: t for t in todos}
        # Reorder based on provided IDs
        reordered = []
        for tid in todo_ids:
            if tid in todo_map:
                reordered.append(todo_map[tid])
        # Add any missing todos at the end (shouldn't happen, but safety)
        for todo in todos:
            if todo['id'] not in todo_ids:
                reordered.append(todo)
        self.save_todos(reordered)
        return True

    # === Launchers ===
    
    def load_launchers(self) -> dict:
        """Load launcher configuration."""
        default = {
            'toolbars': [],
            'current_toolbar': None,
        }
        return self._load_json(self.launchers_file, default)

    def save_launchers(self, launchers: dict):
        """Save launcher configuration."""
        self._save_json(self.launchers_file, launchers)

    def add_toolbar(self, name: str, color: str = '#3498db') -> dict:
        """Add a new toolbar and return it."""
        launchers = self.load_launchers()
        toolbar = {
            'id': str(uuid.uuid4()),
            'name': name,
            'color': color,
            'items': [],
        }
        launchers['toolbars'].append(toolbar)
        self.save_launchers(launchers)
        return toolbar

    def rename_toolbar(self, toolbar_id: str, new_name: str) -> bool:
        """Rename a toolbar."""
        launchers = self.load_launchers()
        for toolbar in launchers['toolbars']:
            if toolbar['id'] == toolbar_id:
                toolbar['name'] = new_name
                self.save_launchers(launchers)
                return True
        return False

    def delete_toolbar(self, toolbar_id: str) -> bool:
        """Delete a toolbar."""
        launchers = self.load_launchers()
        original_len = len(launchers['toolbars'])
        launchers['toolbars'] = [t for t in launchers['toolbars'] if t['id'] != toolbar_id]
        if len(launchers['toolbars']) < original_len:
            self.save_launchers(launchers)
            return True
        return False

    def add_shortcut(self, toolbar_id: str, name: str, path: str, icon_path: str = None) -> dict:
        """Add a shortcut to a toolbar."""
        launchers = self.load_launchers()
        for toolbar in launchers['toolbars']:
            if toolbar['id'] == toolbar_id:
                shortcut = {
                    'id': str(uuid.uuid4()),
                    'type': 'shortcut',
                    'name': name,
                    'path': path,
                    'icon_path': icon_path,
                }
                toolbar['items'].append(shortcut)
                self.save_launchers(launchers)
                return shortcut
        return None

    def delete_shortcut(self, toolbar_id: str, shortcut_id: str) -> bool:
        """Delete a shortcut from a toolbar."""
        launchers = self.load_launchers()
        for toolbar in launchers['toolbars']:
            if toolbar['id'] == toolbar_id:
                original_len = len(toolbar['items'])
                toolbar['items'] = [i for i in toolbar['items'] if i['id'] != shortcut_id]
                if len(toolbar['items']) < original_len:
                    self.save_launchers(launchers)
                    return True
        return False


# Global storage instance
_storage = None


def get_storage() -> StorageManager:
    """Get the global storage manager instance."""
    global _storage
    if _storage is None:
        _storage = StorageManager()
    return _storage
