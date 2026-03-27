"""Main window widget for WinBuddy."""

import logging

from PyQt6.QtCore import Qt, QPoint, QSize, QRect, QEvent, QTimer
from PyQt6.QtGui import QAction, QFont, QPainter, QColor, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..storage import get_storage
from ..autostart import is_auto_start_enabled, toggle_auto_start
from .todo_list import TodoList

logger = logging.getLogger(__name__)

# Resize border width (pixels)
BORDER_WIDTH = 6


class TitleBar(QFrame):
    """Custom title bar for the frameless window."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(32)
        self._setup_ui()

    def _setup_ui(self):
        """Set up the title bar UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(8)

        # App icon/title
        title = QLabel("WinBuddy")
        title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        title.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        layout.addWidget(title)

        layout.addStretch()

        # Minimize button
        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(24, 24)
        self.min_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.min_btn.setToolTip("Minimize to tray")
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.7);
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.min_btn)

        # Close button (minimizes to tray)
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setToolTip("Close to tray")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.7);
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                border-radius: 4px;
                color: white;
            }
        """)
        layout.addWidget(self.close_btn)

        self.setStyleSheet("""
            TitleBar {
                background-color: transparent;
            }
        """)


class MainWindow(QWidget):
    """Main application window - frameless, always-on-top, draggable, resizable."""

    def __init__(self):
        super().__init__()
        self.storage = get_storage()
        self._drag_pos = None
        self._resizing = False
        self._resize_edge = None
        self._resize_start_pos = None
        self._resize_start_geometry = None
        self._user_size = None

        self._setup_window()
        self._setup_ui()
        self._load_position()

    def _setup_window(self):
        """Configure window properties."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        # Don't use WA_TranslucentBackground - it causes click-through issues
        # Instead we'll paint the background ourselves
        
        self.setMinimumSize(250, 200)
        self.setMaximumSize(600, 1200)
        self.setMouseTracking(True)

    def _setup_ui(self):
        """Set up the main UI."""
        # Container with rounded corners
        self.container = QFrame(self)
        self.container.setObjectName("container")
        self.container.setMouseTracking(True)
        
        # Main layout with margin for resize border
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(BORDER_WIDTH, BORDER_WIDTH,
                                       BORDER_WIDTH, BORDER_WIDTH)
        main_layout.addWidget(self.container)

        # Container layout
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Title bar
        self.title_bar = TitleBar()
        self.title_bar.setMouseTracking(True)
        self.title_bar.close_btn.clicked.connect(self.hide)
        self.title_bar.min_btn.clicked.connect(self.hide)
        container_layout.addWidget(self.title_bar)

        # Separator
        separator = QFrame()
        separator.setFixedHeight(1)
        container_layout.addWidget(separator)

        # Content area
        content = QFrame()
        content.setMouseTracking(True)
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 8, 0, 8)
        content_layout.setSpacing(8)

        # Todo list
        self.todo_list = TodoList()
        content_layout.addWidget(self.todo_list)

        container_layout.addWidget(content, 1)

    def paintEvent(self, event):
        """Paint the window background with resize border."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        m = BORDER_WIDTH
        
        # Draw the outer border area (resize zone) - slightly visible
        border_color = QColor(20, 20, 30, 200)
        painter.fillRect(0, 0, w, h, border_color)
        
        # Draw the main container background with rounded corners
        container_rect = QRect(m, m, w - 2*m, h - 2*m)
        bg_color = QColor(30, 30, 40, 242)  # 0.95 opacity
        painter.setBrush(bg_color)
        painter.setPen(QPen(QColor(255, 255, 255, 25), 1))
        painter.drawRoundedRect(container_rect, 12, 12)
        
        # Draw resize grip indicator in bottom-right corner
        grip_color = QColor(255, 255, 255, 40)
        painter.setPen(QPen(grip_color, 2))
        gx, gy = w - 5, h - 5
        for i in range(3):
            painter.drawLine(gx - i*4, gy, gx, gy - i*4)
        
        painter.end()

    # ------------------------------------------------------------------
    # DPI / screen-change handling
    # ------------------------------------------------------------------

    def moveEvent(self, event):
        """Detect when window moves to a different screen (different DPI)."""
        super().moveEvent(event)
        new_screen = QApplication.screenAt(self.geometry().center())
        if new_screen and hasattr(self, '_current_screen'):
            if new_screen != self._current_screen:
                # Screen changed - DPI may be different, schedule size restore
                self._current_screen = new_screen
                if self._user_size and not self._resizing:
                    QTimer.singleShot(100, self._restore_size_after_dpi)
        if new_screen:
            self._current_screen = new_screen

    def _restore_size_after_dpi(self):
        """Re-apply the user-chosen size after a DPI change."""
        if self._user_size and not self._resizing:
            self.resize(self._user_size)

    def resizeEvent(self, event):
        """Track the user-chosen size when user resizes."""
        super().resizeEvent(event)
        # Only update stored size during active user resize, or initial setup
        if self._resizing or not hasattr(self, '_current_screen'):
            self._user_size = self.size()

    # ------------------------------------------------------------------
    # Resize edge detection
    # ------------------------------------------------------------------

    def _get_resize_edge(self, pos):
        """Determine which edge/corner is being hovered for resize."""
        x, y = pos.x(), pos.y()
        w, h = self.width(), self.height()

        left = x < BORDER_WIDTH
        right = x > w - BORDER_WIDTH
        top = y < BORDER_WIDTH
        bottom = y > h - BORDER_WIDTH

        if top and left:
            return 'top-left'
        elif top and right:
            return 'top-right'
        elif bottom and left:
            return 'bottom-left'
        elif bottom and right:
            return 'bottom-right'
        elif left:
            return 'left'
        elif right:
            return 'right'
        elif top:
            return 'top'
        elif bottom:
            return 'bottom'
        return None

    def _update_cursor(self, edge):
        """Update cursor based on resize edge."""
        cursors = {
            'left': Qt.CursorShape.SizeHorCursor,
            'right': Qt.CursorShape.SizeHorCursor,
            'top': Qt.CursorShape.SizeVerCursor,
            'bottom': Qt.CursorShape.SizeVerCursor,
            'top-left': Qt.CursorShape.SizeFDiagCursor,
            'bottom-right': Qt.CursorShape.SizeFDiagCursor,
            'top-right': Qt.CursorShape.SizeBDiagCursor,
            'bottom-left': Qt.CursorShape.SizeBDiagCursor,
        }
        if edge in cursors:
            self.setCursor(cursors[edge])
        else:
            self.unsetCursor()

    # ------------------------------------------------------------------
    # Mouse events for dragging and resizing
    # ------------------------------------------------------------------

    def mousePressEvent(self, event):
        """Start dragging or resizing on mouse press."""
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            edge = self._get_resize_edge(pos)

            if edge:
                # Start resizing
                self._resizing = True
                self._resize_edge = edge
                self._resize_start_pos = event.globalPosition().toPoint()
                self._resize_start_geometry = self.geometry()
                event.accept()
            elif BORDER_WIDTH <= pos.y() < BORDER_WIDTH + 40:
                # Start dragging (title bar area)
                self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        """Handle dragging or resizing."""
        pos = event.position().toPoint()

        if self._resizing and event.buttons() == Qt.MouseButton.LeftButton:
            # Handle resize
            delta = event.globalPosition().toPoint() - self._resize_start_pos
            geo = QRect(self._resize_start_geometry)

            min_w, min_h = self.minimumWidth(), self.minimumHeight()
            max_w, max_h = self.maximumWidth(), self.maximumHeight()

            if 'left' in self._resize_edge:
                new_left = geo.left() + delta.x()
                new_width = geo.right() - new_left + 1
                if min_w <= new_width <= max_w:
                    geo.setLeft(new_left)
            if 'right' in self._resize_edge:
                new_width = geo.width() + delta.x()
                if min_w <= new_width <= max_w:
                    geo.setWidth(new_width)
            if 'top' in self._resize_edge:
                new_top = geo.top() + delta.y()
                new_height = geo.bottom() - new_top + 1
                if min_h <= new_height <= max_h:
                    geo.setTop(new_top)
            if 'bottom' in self._resize_edge:
                new_height = geo.height() + delta.y()
                if min_h <= new_height <= max_h:
                    geo.setHeight(new_height)

            self.setGeometry(geo)
            self._user_size = self.size()
            event.accept()
        elif self._drag_pos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            # Handle dragging
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        else:
            # Update cursor based on position
            edge = self._get_resize_edge(pos)
            self._update_cursor(edge)

    def mouseReleaseEvent(self, event):
        """End dragging or resizing on mouse release."""
        if event.button() == Qt.MouseButton.LeftButton:
            if self._resizing or self._drag_pos:
                self._save_position()
            self._drag_pos = None
            self._resizing = False
            self._resize_edge = None

    def show_and_raise(self):
        self.show()
        self.raise_()
        self.activateWindow()

    # ------------------------------------------------------------------
    # Position / size persistence
    # ------------------------------------------------------------------

    def _load_position(self):
        """Load saved window position and size."""
        settings = self.storage.load_settings()
        x = settings.get('window_x', 100)
        y = settings.get('window_y', 100)
        w = settings.get('window_width', 300)
        h = settings.get('window_height', 500)

        self.resize(w, h)
        self._user_size = QSize(w, h)

        screen = QApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            x = max(geo.left(), min(x, geo.right() - self.width()))
            y = max(geo.top(), min(y, geo.bottom() - self.height()))

        self.move(x, y)

    def _save_position(self):
        """Save current window position and size."""
        settings = self.storage.load_settings()
        settings['window_x'] = self.x()
        settings['window_y'] = self.y()
        settings['window_width'] = self.width()
        settings['window_height'] = self.height()
        self.storage.save_settings(settings)

    # ------------------------------------------------------------------
    # Close / context menu
    # ------------------------------------------------------------------

    def closeEvent(self, event):
        """Hide to tray instead of closing."""
        event.ignore()
        self.hide()

    def contextMenuEvent(self, event):
        """Show context menu on right-click in title bar."""
        if event.pos().y() < BORDER_WIDTH + 40:
            menu = QMenu(self)

            hide_action = menu.addAction("Hide Reminders")
            hide_action.triggered.connect(self.hide)

            menu.addSeparator()

            autostart = menu.addAction("Start with Windows")
            autostart.setCheckable(True)
            autostart.setChecked(is_auto_start_enabled())
            autostart.triggered.connect(
                lambda: toggle_auto_start()
            )

            menu.exec(event.globalPos())
