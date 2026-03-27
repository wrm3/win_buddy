"""Windows auto-start functionality for WinBuddy."""

import logging
import os
import sys

logger = logging.getLogger(__name__)

# Registry key for current user startup
STARTUP_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_NAME = "WinBuddy"


def get_app_path() -> str:
    """Get the path to launch the app."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys.executable
    else:
        # Running as script - use pythonw to avoid console
        python = sys.executable
        if python.endswith('python.exe'):
            pythonw = python.replace('python.exe', 'pythonw.exe')
            if os.path.exists(pythonw):
                python = pythonw
        main_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'main.py'))
        return f'"{python}" "{main_script}"'


def is_auto_start_enabled() -> bool:
    """Check if auto-start is enabled in Windows registry."""
    if os.name != 'nt':
        logger.warning("Auto-start only supported on Windows")
        return False
    
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, APP_NAME)
            return True
        except FileNotFoundError:
            return False
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        logger.error(f"Error checking auto-start: {e}")
        return False


def enable_auto_start() -> bool:
    """Enable auto-start by adding registry entry."""
    if os.name != 'nt':
        logger.warning("Auto-start only supported on Windows")
        return False
    
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_SET_VALUE)
        try:
            app_path = get_app_path()
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, app_path)
            logger.info(f"Auto-start enabled: {app_path}")
            return True
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        logger.error(f"Error enabling auto-start: {e}")
        return False


def disable_auto_start() -> bool:
    """Disable auto-start by removing registry entry."""
    if os.name != 'nt':
        logger.warning("Auto-start only supported on Windows")
        return False
    
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, STARTUP_KEY, 0, winreg.KEY_SET_VALUE)
        try:
            winreg.DeleteValue(key, APP_NAME)
            logger.info("Auto-start disabled")
            return True
        except FileNotFoundError:
            # Already not set
            return True
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        logger.error(f"Error disabling auto-start: {e}")
        return False


def toggle_auto_start() -> bool:
    """Toggle auto-start and return new state."""
    if is_auto_start_enabled():
        disable_auto_start()
        return False
    else:
        enable_auto_start()
        return True
