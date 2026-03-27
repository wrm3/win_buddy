"""Todo list widget for WinBuddy."""

from PyQt6.QtCore import Qt, pyqtSignal, QEvent, QMimeData, QPoint, QSize
from PyQt6.QtGui import QFont, QKeyEvent, QDrag, QPainter, QPixmap, QColor, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QApplication,
)

from ..storage import get_storage

# Color cycle for the indicator dot
DOT_COLORS = ['#cccccc', '#ef4444', '#f59e0b', '#22c55e', '#3b82f6', '#a855f7']


class ColorDot(QWidget):
    """A small clickable colored circle that cycles through colors."""
    
    color_changed = pyqtSignal(str)  # Emits new color hex
    
    def __init__(self, color: str = '#cccccc', parent=None):
        super().__init__(parent)
        self._color = color if color in DOT_COLORS else '#cccccc'
        self.setFixedSize(14, 14)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Click to change color")
    
    def sizeHint(self):
        return QSize(14, 14)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor(self._color)
        # Draw filled circle
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(130), 1))
        painter.drawEllipse(1, 1, 11, 11)
        painter.end()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Cycle to next color
            try:
                idx = DOT_COLORS.index(self._color)
            except ValueError:
                idx = -1
            self._color = DOT_COLORS[(idx + 1) % len(DOT_COLORS)]
            self.update()
            self.color_changed.emit(self._color)
            event.accept()
    
    def set_color(self, color: str):
        self._color = color if color in DOT_COLORS else '#cccccc'
        self.update()


class TodoItem(QFrame):
    """A single todo item widget with drag support."""
    
    deleted = pyqtSignal(str)  # Emits todo_id
    edited = pyqtSignal(str, str)  # Emits todo_id, new_text
    color_changed = pyqtSignal(str, str)  # Emits todo_id, new_color
    drag_started = pyqtSignal(object)  # Emits self
    
    def __init__(self, todo_data: dict, parent=None):
        super().__init__(parent)
        self.todo_id = todo_data['id']
        self.todo_text = todo_data['text']
        self.completed = todo_data.get('completed', False)
        self.todo_color = todo_data.get('color', '#cccccc')
        
        self._drag_start_pos = None
        self._is_editing = False
        
        self._setup_ui()
        self._apply_style()
    
    def _setup_ui(self):
        """Set up the todo item UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(6)
        
        # Color indicator dot
        self.color_dot = ColorDot(self.todo_color)
        self.color_dot.color_changed.connect(self._on_color_changed)
        layout.addWidget(self.color_dot)
        
        # Drag handle
        self.drag_handle = QLabel("⋮⋮")
        self.drag_handle.setFixedWidth(14)
        self.drag_handle.setCursor(Qt.CursorShape.OpenHandCursor)
        self.drag_handle.setStyleSheet("color: rgba(255, 255, 255, 0.4); font-size: 12px;")
        self.drag_handle.setToolTip("Drag to reorder")
        layout.addWidget(self.drag_handle)
        
        # Text label (double-click to edit)
        self.text_label = QLabel(self.todo_text)
        self.text_label.setWordWrap(True)
        self.text_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.text_label.setToolTip("Double-click to edit")
        layout.addWidget(self.text_label, 1)
        
        # Edit input (hidden by default)
        self.edit_input = QLineEdit()
        self.edit_input.setVisible(False)
        self.edit_input.returnPressed.connect(self._save_edit)
        self.edit_input.installEventFilter(self)
        layout.addWidget(self.edit_input, 1)
        
        # Edit button
        self.edit_btn = QPushButton("✎")
        self.edit_btn.setFixedSize(24, 24)
        self.edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.edit_btn.setToolTip("Edit")
        self.edit_btn.clicked.connect(lambda: self._start_edit(None))
        layout.addWidget(self.edit_btn)
        
        # Delete button
        self.delete_btn = QPushButton("×")
        self.delete_btn.setFixedSize(24, 24)
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.setToolTip("Delete")
        self.delete_btn.clicked.connect(self._on_delete)
        layout.addWidget(self.delete_btn)
        
        # Double-click to edit
        self.text_label.mouseDoubleClickEvent = self._start_edit
    
    def _apply_style(self):
        """Apply styling to the todo item."""
        self.setStyleSheet("""
            TodoItem {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 6px;
                margin: 2px;
            }
            TodoItem:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
            QLabel {
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 4px;
                color: #ffffff;
                padding: 4px;
            }
            QPushButton#delete_btn {
                background-color: transparent;
                border: none;
                color: #ff6b6b;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton#delete_btn:hover {
                color: #ff4444;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: rgba(255, 255, 255, 0.6);
                font-size: 14px;
            }
            QPushButton:hover {
                color: #ffffff;
            }
        """)
        
        if self.completed:
            self.text_label.setStyleSheet("color: #888888; text-decoration: line-through;")
    
    def eventFilter(self, obj, event):
        """Handle escape key to cancel editing."""
        if obj == self.edit_input and event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Escape:
                self._cancel_edit()
                return True
        return super().eventFilter(obj, event)
    
    def mousePressEvent(self, event):
        """Handle mouse press for drag initiation."""
        if event.button() == Qt.MouseButton.LeftButton and not self._is_editing:
            # Check if clicking on the drag handle widget area
            handle_geo = self.drag_handle.geometry()
            click_x = event.position().x()
            if handle_geo.left() - 4 <= click_x <= handle_geo.right() + 4:
                self._drag_start_pos = event.position().toPoint()
                self.drag_handle.setCursor(Qt.CursorShape.ClosedHandCursor)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging."""
        if self._drag_start_pos is not None:
            # Check if moved enough to start drag
            diff = event.position().toPoint() - self._drag_start_pos
            if diff.manhattanLength() > QApplication.startDragDistance():
                self._start_drag()
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release."""
        self._drag_start_pos = None
        self.drag_handle.setCursor(Qt.CursorShape.OpenHandCursor)
        super().mouseReleaseEvent(event)
    
    def _start_drag(self):
        """Initiate drag operation."""
        self._drag_start_pos = None
        
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.todo_id)
        drag.setMimeData(mime_data)
        
        # Create a semi-transparent pixmap of this widget
        pixmap = QPixmap(self.size())
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setOpacity(0.7)
        self.render(painter)
        painter.end()
        
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
        
        # Emit signal so parent knows drag started
        self.drag_started.emit(self)
        
        # Execute drag
        drag.exec(Qt.DropAction.MoveAction)
        
        self.drag_handle.setCursor(Qt.CursorShape.OpenHandCursor)
    
    def _on_color_changed(self, new_color: str):
        """Handle color dot click."""
        self.todo_color = new_color
        self.color_changed.emit(self.todo_id, new_color)
    
    def _start_edit(self, event):
        """Start editing the todo text."""
        self._is_editing = True
        self.text_label.setVisible(False)
        self.edit_btn.setVisible(False)
        self.drag_handle.setVisible(False)
        self.color_dot.setVisible(False)
        self.edit_input.setVisible(True)
        self.edit_input.setText(self.todo_text)
        self.edit_input.setFocus()
        self.edit_input.selectAll()
    
    def _cancel_edit(self):
        """Cancel editing without saving."""
        self._is_editing = False
        self.edit_input.setVisible(False)
        self.text_label.setVisible(True)
        self.edit_btn.setVisible(True)
        self.drag_handle.setVisible(True)
        self.color_dot.setVisible(True)
    
    def _save_edit(self):
        """Save the edited text."""
        new_text = self.edit_input.text().strip()
        if new_text and new_text != self.todo_text:
            self.todo_text = new_text
            self.text_label.setText(new_text)
            self.edited.emit(self.todo_id, new_text)
        
        self._is_editing = False
        self.edit_input.setVisible(False)
        self.text_label.setVisible(True)
        self.edit_btn.setVisible(True)
        self.drag_handle.setVisible(True)
        self.color_dot.setVisible(True)
    
    def _on_delete(self):
        """Handle delete button click."""
        self.deleted.emit(self.todo_id)


class DropIndicator(QFrame):
    """Visual indicator for drop position."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)
        self.setStyleSheet("""
            DropIndicator {
                background-color: #4CAF50;
                border-radius: 2px;
            }
        """)
        self.hide()


class TodoList(QFrame):
    """Main todo list container widget with drag-and-drop reordering."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = get_storage()
        self._dragging_item = None
        self._setup_ui()
        self._load_todos()
    
    def _setup_ui(self):
        """Set up the todo list UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header
        header = QHBoxLayout()
        
        title = QLabel("📋 Reminders")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff;")
        header.addWidget(title)
        
        header.addStretch()
        
        # Add button
        self.add_btn = QPushButton("+")
        self.add_btn.setFixedSize(28, 28)
        self.add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_btn.clicked.connect(self._show_add_input)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                border-radius: 14px;
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        header.addWidget(self.add_btn)
        
        layout.addLayout(header)
        
        # Add input (hidden by default)
        self.add_input = QLineEdit()
        self.add_input.setPlaceholderText("What do you need to remember?")
        self.add_input.setVisible(False)
        self.add_input.returnPressed.connect(self._add_todo)
        self.add_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                color: #ffffff;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        layout.addWidget(self.add_input)
        
        # Scroll area for todos
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: transparent;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Container for todo items - enable drops
        self.todo_container = QWidget()
        self.todo_container.setAcceptDrops(True)
        self.todo_layout = QVBoxLayout(self.todo_container)
        self.todo_layout.setContentsMargins(0, 0, 0, 0)
        self.todo_layout.setSpacing(4)
        self.todo_layout.addStretch()
        
        # Drop indicator
        self.drop_indicator = DropIndicator(self.todo_container)
        
        # Override drag/drop events on container
        self.todo_container.dragEnterEvent = self._on_drag_enter
        self.todo_container.dragMoveEvent = self._on_drag_move
        self.todo_container.dragLeaveEvent = self._on_drag_leave
        self.todo_container.dropEvent = self._on_drop
        
        scroll.setWidget(self.todo_container)
        layout.addWidget(scroll, 1)
        
        # Empty state
        self.empty_label = QLabel("No reminders yet.\nClick + to add one!")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setStyleSheet("color: rgba(255, 255, 255, 0.5); font-size: 12px;")
        self.todo_layout.insertWidget(0, self.empty_label)
        
        self.setMinimumHeight(150)
        self.setMaximumHeight(900)
    
    def _load_todos(self):
        """Load todos from storage."""
        todos = self.storage.load_todos()
        for todo in todos:
            self._add_todo_widget(todo)
        self._update_empty_state()
    
    def _add_todo_widget(self, todo_data: dict, at_top: bool = False):
        """Add a todo item widget.
        
        Args:
            todo_data: The todo item data dict.
            at_top: If True, insert at the top of the list (for new items).
        """
        item = TodoItem(todo_data)
        item.deleted.connect(self._on_delete_todo)
        item.edited.connect(self._on_edit_todo)
        item.color_changed.connect(self._on_color_changed)
        item.drag_started.connect(self._on_drag_started)
        
        if at_top:
            # Insert at position 0 (top of list, after empty_label which hides itself)
            self.todo_layout.insertWidget(0, item)
        else:
            # Insert before the stretch (append to bottom - used when loading)
            self.todo_layout.insertWidget(self.todo_layout.count() - 1, item)
        self._update_empty_state()
    
    def _show_add_input(self):
        """Show the add input field."""
        self.add_input.setVisible(True)
        self.add_input.setFocus()
    
    def _add_todo(self):
        """Add a new todo from the input."""
        text = self.add_input.text().strip()
        if text:
            todo = self.storage.add_todo(text)
            self._add_todo_widget(todo, at_top=True)
            self.add_input.clear()
        self.add_input.setVisible(False)
    
    def _on_delete_todo(self, todo_id: str):
        """Handle todo deletion."""
        self.storage.delete_todo(todo_id)
        
        # Find and remove the widget
        for i in range(self.todo_layout.count()):
            widget = self.todo_layout.itemAt(i).widget()
            if isinstance(widget, TodoItem) and widget.todo_id == todo_id:
                widget.deleteLater()
                break
        
        self._update_empty_state()
    
    def _on_edit_todo(self, todo_id: str, new_text: str):
        """Handle todo edit."""
        self.storage.update_todo(todo_id, new_text)
    
    def _on_color_changed(self, todo_id: str, new_color: str):
        """Handle color dot change."""
        self.storage.update_todo_color(todo_id, new_color)
    
    def _update_empty_state(self):
        """Show/hide empty state label."""
        has_todos = any(
            isinstance(self.todo_layout.itemAt(i).widget(), TodoItem)
            for i in range(self.todo_layout.count())
        )
        self.empty_label.setVisible(not has_todos)
    
    def _on_drag_started(self, item):
        """Handle drag start from a todo item."""
        self._dragging_item = item
    
    def _get_todo_items(self):
        """Get list of TodoItem widgets in order."""
        items = []
        for i in range(self.todo_layout.count()):
            widget = self.todo_layout.itemAt(i).widget()
            if isinstance(widget, TodoItem):
                items.append(widget)
        return items
    
    def _find_drop_index(self, pos):
        """Find the index where a drop should occur based on position."""
        items = self._get_todo_items()
        if not items:
            return 0
        
        for i, item in enumerate(items):
            item_rect = item.geometry()
            item_center_y = item_rect.top() + item_rect.height() // 2
            if pos.y() < item_center_y:
                return i
        
        return len(items)
    
    def _on_drag_enter(self, event):
        """Handle drag enter."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
    
    def _on_drag_move(self, event):
        """Handle drag move - show indicator."""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
            # Find drop position
            drop_index = self._find_drop_index(event.position().toPoint())
            items = self._get_todo_items()
            
            # Position the indicator
            if items:
                if drop_index < len(items):
                    target_item = items[drop_index]
                    indicator_y = target_item.geometry().top() - 4
                else:
                    # After last item
                    target_item = items[-1]
                    indicator_y = target_item.geometry().bottom() + 2
                
                self.drop_indicator.setGeometry(
                    4, indicator_y,
                    self.todo_container.width() - 8, 4
                )
                self.drop_indicator.show()
    
    def _on_drag_leave(self, event):
        """Handle drag leave - hide indicator."""
        self.drop_indicator.hide()
    
    def _on_drop(self, event):
        """Handle drop - reorder items."""
        self.drop_indicator.hide()
        
        if event.mimeData().hasText():
            dropped_id = event.mimeData().text()
            drop_index = self._find_drop_index(event.position().toPoint())
            
            # Get current order of items
            items = self._get_todo_items()
            current_ids = [item.todo_id for item in items]
            
            # Find the dragged item's current index
            if dropped_id not in current_ids:
                return
            
            old_index = current_ids.index(dropped_id)
            
            # Don't do anything if dropped at same position
            if old_index == drop_index or old_index == drop_index - 1:
                event.acceptProposedAction()
                return
            
            # Calculate new order
            current_ids.remove(dropped_id)
            if drop_index > old_index:
                drop_index -= 1
            current_ids.insert(drop_index, dropped_id)
            
            # Save new order
            self.storage.reorder_todos(current_ids)
            
            # Rebuild the UI in new order
            self._rebuild_todo_list()
            
            event.acceptProposedAction()
    
    def _rebuild_todo_list(self):
        """Rebuild the todo list from storage (after reorder)."""
        # Remove all current items
        items_to_remove = self._get_todo_items()
        for item in items_to_remove:
            item.deleteLater()
        
        # Reload from storage
        todos = self.storage.load_todos()
        for todo in todos:
            self._add_todo_widget(todo)
        
        self._update_empty_state()
