"""WinBuddy - Floating productivity widgets.

Two independent floating widgets:
1. Reminders - A quick to-do reminder list
2. Quick Launcher - A hexagonal app launcher

Usage:
    uv run python main.py
"""

import logging
import sys

from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QRect

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def center_on_screen(widget):
    """Move a widget to the center of its current (or primary) screen."""
    screen = QApplication.screenAt(widget.geometry().center())
    if not screen:
        screen = QApplication.primaryScreen()
    geo = screen.availableGeometry()
    x = geo.x() + (geo.width() - widget.width()) // 2
    y = geo.y() + (geo.height() - widget.height()) // 2
    widget.move(x, y)
    widget.show()
    widget.raise_()
    widget.activateWindow()


def ensure_on_screen(widget):
    """If the widget is completely off every visible screen, center it on the primary."""
    widget_rect = widget.frameGeometry()
    for screen in QApplication.screens():
        if screen.availableGeometry().intersects(widget_rect):
            return  # at least partially visible
    logger.info(f"Window '{widget.windowTitle()}' was off-screen, recentering.")
    center_on_screen(widget)


def main():
    """Main entry point for WinBuddy."""
    logger.info("Starting WinBuddy...")
    
    # Create application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Keep running in tray
    
    # Set application metadata
    app.setApplicationName("WinBuddy")
    app.setApplicationVersion("0.1.0")
    app.setOrganizationName("WinBuddy")
    
    # Apply dark theme
    app.setStyle("Fusion")
    
    # Import widgets
    from src.winbuddy.widgets import MainWindow, LauncherWindow
    from src.winbuddy.autostart import is_auto_start_enabled, toggle_auto_start
    
    # Create both windows
    reminders_window = MainWindow()
    launcher_window = LauncherWindow()
    
    # Show both and ensure they're on a visible screen
    reminders_window.show()
    launcher_window.show()
    ensure_on_screen(reminders_window)
    ensure_on_screen(launcher_window)
    
    # ------------------------------------------------------------------
    # Single unified tray icon (yellow folder / WinBuddy Launcher icon)
    # ------------------------------------------------------------------
    tray_icon = QSystemTrayIcon()
    icon = app.style().standardIcon(
        app.style().StandardPixmap.SP_FileDialogStart
    )
    tray_icon.setIcon(icon)
    tray_icon.setToolTip("WinBuddy")
    
    tray_menu = QMenu()
    
    # -- Reminders section --
    reminders_header = QAction("── Reminders ──", None)
    reminders_header.setEnabled(False)
    tray_menu.addAction(reminders_header)
    
    show_reminders = QAction("Show Reminders", None)
    show_reminders.triggered.connect(reminders_window.show_and_raise)
    tray_menu.addAction(show_reminders)
    
    hide_reminders = QAction("Hide Reminders", None)
    hide_reminders.triggered.connect(reminders_window.hide)
    tray_menu.addAction(hide_reminders)
    
    center_reminders = QAction("Center Reminders", None)
    center_reminders.triggered.connect(lambda: center_on_screen(reminders_window))
    tray_menu.addAction(center_reminders)
    
    # -- Launcher section --
    launcher_header = QAction("── Launcher ──", None)
    launcher_header.setEnabled(False)
    tray_menu.addAction(launcher_header)
    
    show_launcher = QAction("Show Launcher", None)
    show_launcher.triggered.connect(launcher_window.show_and_raise)
    tray_menu.addAction(show_launcher)
    
    hide_launcher = QAction("Hide Launcher", None)
    hide_launcher.triggered.connect(launcher_window.hide)
    tray_menu.addAction(hide_launcher)
    
    center_launcher = QAction("Center Launcher", None)
    center_launcher.triggered.connect(lambda: center_on_screen(launcher_window))
    tray_menu.addAction(center_launcher)
    
    # -- WinBuddy section --
    winbuddy_header = QAction("── WinBuddy ──", None)
    winbuddy_header.setEnabled(False)
    tray_menu.addAction(winbuddy_header)
    
    show_all = QAction("Show All", None)
    show_all.triggered.connect(
        lambda: (reminders_window.show_and_raise(),
                 launcher_window.show_and_raise())
    )
    tray_menu.addAction(show_all)
    
    hide_all = QAction("Hide All", None)
    hide_all.triggered.connect(
        lambda: (reminders_window.hide(),
                 launcher_window.hide())
    )
    tray_menu.addAction(hide_all)
    
    autostart_action = QAction("Start with Windows", None)
    autostart_action.setCheckable(True)
    autostart_action.setChecked(is_auto_start_enabled())
    autostart_action.triggered.connect(
        lambda: autostart_action.setChecked(toggle_auto_start())
    )
    tray_menu.addAction(autostart_action)
    
    def quit_all():
        reminders_window._save_position()
        launcher_window._save_position()
        launcher_window.close_all_petals()
        reminders_window.close()
        launcher_window.close()
        tray_icon.hide()
        app.quit()
    
    exit_action = QAction("Exit WinBuddy", None)
    exit_action.triggered.connect(quit_all)
    tray_menu.addAction(exit_action)
    
    tray_icon.setContextMenu(tray_menu)
    
    # Double-click tray icon → show everything
    tray_icon.activated.connect(
        lambda reason: (
            reminders_window.show_and_raise(),
            launcher_window.show_and_raise()
        ) if reason == QSystemTrayIcon.ActivationReason.Trigger else None
    )
    tray_icon.show()
    
    logger.info("WinBuddy is running. Right-click the tray icon for options.")
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
