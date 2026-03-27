"""Icon extraction utilities for WinBuddy."""

import logging
import os
import sys
from pathlib import Path
from functools import lru_cache

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QFileIconProvider, QApplication
from PyQt6.QtCore import QFileInfo

logger = logging.getLogger(__name__)

# Cache for extracted icons
_icon_cache = {}


def get_icon_for_path(path: str, size: int = 32) -> QIcon:
    """Get an icon for a file path, with caching."""
    if not path:
        return QIcon()
    
    # Check cache
    cache_key = f"{path}_{size}"
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]
    
    icon = QIcon()
    
    try:
        if os.path.exists(path):
            # Use QFileIconProvider for file icons
            provider = QFileIconProvider()
            file_info = QFileInfo(path)
            icon = provider.icon(file_info)
            
            # For .lnk files, try to get the target's icon
            if path.lower().endswith('.lnk'):
                target_icon = _get_shortcut_icon(path)
                if not target_icon.isNull():
                    icon = target_icon
        elif path.startswith('http'):
            # Web URL - use a globe icon
            icon = QApplication.style().standardIcon(
                QApplication.style().StandardPixmap.SP_DriveNetIcon
            )
    except Exception as e:
        logger.debug(f"Error getting icon for {path}: {e}")
    
    # Cache the result
    _icon_cache[cache_key] = icon
    return icon


def _get_shortcut_icon(lnk_path: str) -> QIcon:
    """Extract icon from a Windows .lnk shortcut file."""
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lnk_path)
        target = shortcut.TargetPath
        
        if target and os.path.exists(target):
            provider = QFileIconProvider()
            file_info = QFileInfo(target)
            return provider.icon(file_info)
    except Exception as e:
        logger.debug(f"Error extracting shortcut icon: {e}")
    
    return QIcon()


def get_folder_icon() -> QIcon:
    """Get a folder icon."""
    return QApplication.style().standardIcon(
        QApplication.style().StandardPixmap.SP_DirIcon
    )


def get_default_app_icon() -> QIcon:
    """Get a default application icon."""
    return QApplication.style().standardIcon(
        QApplication.style().StandardPixmap.SP_ComputerIcon
    )
