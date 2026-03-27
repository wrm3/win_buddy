"""Hexagonal radial launcher widget for WinBuddy - Sexy hex design with blooming petals."""

import math
import os
from pathlib import Path

from PyQt6.QtCore import (
    QPoint,
    QPointF,
    Qt,
    QSize,
    QRectF,
    QTimer,
)
from PyQt6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPen,
    QBrush,
    QLinearGradient,
    QRadialGradient,
    QAction,
    QPainterPath,
    QFontMetrics,
    QTransform,
)
from PyQt6.QtWidgets import (
    QApplication,
    QInputDialog,
    QMenu,
    QMessageBox,
    QWidget,
    QToolButton,
    QGraphicsDropShadowEffect,
)

from ..storage import get_storage
from ..icons import get_icon_for_path, get_default_app_icon


class PetalWindow(QWidget):
    """A separate window showing icons for a toolbar - blooms from a segment."""
    
    def __init__(self, toolbar_data: dict, segment_index: int, parent_pos: QPoint):
        super().__init__()
        self.toolbar = toolbar_data
        self.segment_index = segment_index
        self.storage = get_storage()
        self.icon_buttons = []
        
        # Calculate rotation so flat side faces center
        # Segment 0 is at top, segment rotations: 0°, 60°, 120°, 180°, 240°, 300°
        self.rotation_angle = segment_index * 60  # degrees
        
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.setFixedSize(200, 200)
        
        # Position blooming outward from the segment
        self._position_from_parent(parent_pos)
        
        # Glow effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setColor(QColor(toolbar_data.get('color', '#3498db')))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        
        # Create icon buttons after positioning
        QTimer.singleShot(10, self._create_icons)
    
    def _position_from_parent(self, parent_center: QPoint):
        """Position this petal blooming outward from its segment."""
        # Direction this segment faces (segment 0 is top, going clockwise)
        mid_angle = -math.pi / 2 + self.segment_index * math.pi / 3
        
        # Distance from parent center to petal center
        bloom_distance = 170
        
        offset_x = int(bloom_distance * math.cos(mid_angle))
        offset_y = int(bloom_distance * math.sin(mid_angle))
        
        # Position petal center
        petal_x = parent_center.x() + offset_x - 100  # 100 = half of petal width
        petal_y = parent_center.y() + offset_y - 100  # 100 = half of petal height
        
        self.move(petal_x, petal_y)
    
    def _hex_path_rotated(self, center: QPointF, radius: float, rotation_deg: float) -> QPainterPath:
        """Create a hexagon path rotated so flat side faces a direction."""
        path = QPainterPath()
        # Base angle offset to make flat side face the center
        # Adding rotation based on segment position
        base_angle = math.radians(rotation_deg) + math.pi / 6
        
        for i in range(6):
            angle = base_angle + i * math.pi / 3
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()
        return path
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = QPointF(self.width() / 2, self.height() / 2)
        
        # Background hex - rotated so flat side faces parent center
        hex_path = self._hex_path_rotated(center, 95, self.rotation_angle)
        
        color = QColor(self.toolbar.get('color', '#3498db'))
        grad = QRadialGradient(center, 95)
        grad.setColorAt(0, QColor(35, 40, 55, 245))
        grad.setColorAt(0.7, QColor(30, 35, 50, 245))
        grad.setColorAt(1, color.darker(200))
        
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(color, 2))
        painter.drawPath(hex_path)
        
        # Title - position based on rotation
        painter.setPen(Qt.GlobalColor.white)
        font = QFont("Segoe UI", 9, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Draw title in center-top area
        painter.drawText(QRectF(0, 15, self.width(), 20),
                        Qt.AlignmentFlag.AlignCenter, 
                        self.toolbar.get('name', ''))
        
        # Close hint at bottom
        painter.setPen(QColor(140, 150, 170))
        font = QFont("Segoe UI", 7)
        painter.setFont(font)
        painter.drawText(QRectF(0, self.height() - 25, self.width(), 16),
                        Qt.AlignmentFlag.AlignCenter, "click empty to close")
    
    def _create_icons(self):
        """Create icon buttons arranged in the petal."""
        items = self.toolbar.get('items', [])
        center = QPointF(self.width() / 2, self.height() / 2)
        
        # Position icons in rings
        positions = []
        
        # Center position
        positions.append((center.x(), center.y()))
        
        # Ring 1 (6 positions)
        ring1_r = 40
        for i in range(6):
            angle = -math.pi / 2 + i * math.pi / 3
            positions.append((center.x() + ring1_r * math.cos(angle),
                            center.y() + ring1_r * math.sin(angle)))
        
        # Ring 2 (6 positions, offset)
        ring2_r = 70
        for i in range(6):
            angle = -math.pi / 2 + i * math.pi / 3 + math.pi / 6
            positions.append((center.x() + ring2_r * math.cos(angle),
                            center.y() + ring2_r * math.sin(angle)))
        
        shortcut_idx = 0
        for item in items:
            if item.get('type') != 'shortcut':
                continue
            if shortcut_idx >= len(positions):
                break
            
            x, y = positions[shortcut_idx]
            btn = QToolButton(self)
            btn.setFixedSize(32, 32)
            btn.setIconSize(QSize(22, 22))
            btn.move(int(x - 16), int(y - 16))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setToolTip(item.get('name', 'Unknown'))
            
            path = item.get('path', '')
            try:
                icon = get_icon_for_path(path)
                if icon.isNull():
                    icon = get_default_app_icon()
            except Exception:
                icon = get_default_app_icon()
            btn.setIcon(icon)
            
            btn.setStyleSheet("""
                QToolButton {
                    background-color: rgba(50, 55, 70, 0.9);
                    border: 2px solid rgba(100, 120, 150, 0.5);
                    border-radius: 16px;
                }
                QToolButton:hover {
                    background-color: rgba(70, 80, 100, 0.95);
                    border: 2px solid rgba(140, 170, 210, 0.9);
                }
            """)
            
            item_data = item
            btn.clicked.connect(lambda checked, d=item_data: self._launch_shortcut(d))
            btn.show()
            self.icon_buttons.append(btn)
            shortcut_idx += 1
    
    def _launch_shortcut(self, shortcut_data):
        """Launch a shortcut."""
        path = shortcut_data.get('path', '')
        if path and os.path.exists(path):
            try:
                os.startfile(path)
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not launch: {e}")
        elif path.startswith('http'):
            import webbrowser
            webbrowser.open(path)
    
    def mousePressEvent(self, event):
        # Close on any click not on a button
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if click is on empty area (not on buttons)
            click_pos = event.position().toPoint()
            for btn in self.icon_buttons:
                if btn.geometry().contains(click_pos):
                    return  # Let button handle it
            # Close this petal
            self.close()


class HexLauncherWidget(QWidget):
    """The main hex launcher - center hub with blooming petals."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.storage = get_storage()
        self._state = 'collapsed'  # collapsed, expanded
        self._hovered_segment = -1
        self.open_petals = {}  # segment_index -> PetalWindow
        
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        
        self._collapsed_size = 100
        self._expanded_size = 240
        
        self.setFixedSize(self._collapsed_size, self._collapsed_size)
        
        # Glow effect
        self.glow = QGraphicsDropShadowEffect()
        self.glow.setBlurRadius(25)
        self.glow.setColor(QColor(52, 152, 219, 120))
        self.glow.setOffset(0, 0)
        self.setGraphicsEffect(self.glow)
    
    def _get_center(self):
        return QPointF(self.width() / 2, self.height() / 2)
    
    def _get_global_center(self):
        """Get the center of this widget in global screen coordinates."""
        local_center = QPoint(self.width() // 2, self.height() // 2)
        return self.mapToGlobal(local_center)
    
    def _hex_path(self, center: QPointF, radius: float) -> QPainterPath:
        """Create a hexagon path."""
        path = QPainterPath()
        for i in range(6):
            angle = math.pi / 6 + i * math.pi / 3
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            if i == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.closeSubpath()
        return path
    
    def _get_segment_path(self, index: int, inner_r: float, outer_r: float) -> QPainterPath:
        """Get the path for a trapezoid segment."""
        center = self._get_center()
        angle_start = -math.pi / 2 + index * math.pi / 3 - math.pi / 6
        angle_end = angle_start + math.pi / 3
        
        gap = 0.03
        angle_start += gap
        angle_end -= gap
        
        p1 = QPointF(center.x() + inner_r * math.cos(angle_start),
                     center.y() + inner_r * math.sin(angle_start))
        p2 = QPointF(center.x() + outer_r * math.cos(angle_start),
                     center.y() + outer_r * math.sin(angle_start))
        p3 = QPointF(center.x() + outer_r * math.cos(angle_end),
                     center.y() + outer_r * math.sin(angle_end))
        p4 = QPointF(center.x() + inner_r * math.cos(angle_end),
                     center.y() + inner_r * math.sin(angle_end))
        
        path = QPainterPath()
        path.moveTo(p1)
        path.lineTo(p2)
        path.lineTo(p3)
        path.lineTo(p4)
        path.closeSubpath()
        return path
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self._get_center()
        
        if self._state == 'collapsed':
            self._draw_collapsed(painter, center)
        elif self._state == 'expanded':
            self._draw_expanded(painter, center)
    
    def _draw_collapsed(self, painter: QPainter, center: QPointF):
        """Draw collapsed state - just the center hex."""
        radius = 40
        
        # Outer ring
        ring_path = self._hex_path(center, 48)
        painter.setBrush(QBrush(QColor(50, 60, 80, 200)))
        painter.setPen(QPen(QColor(80, 100, 130), 2))
        painter.drawPath(ring_path)
        
        # Center hex
        hex_path = self._hex_path(center, radius)
        grad = QRadialGradient(center, radius)
        grad.setColorAt(0, QColor(60, 70, 90))
        grad.setColorAt(1, QColor(40, 50, 70))
        
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(100, 130, 170), 2))
        painter.drawPath(hex_path)
        
        # Center icon
        painter.setPen(QColor(140, 170, 210))
        font = QFont("Segoe UI", 18)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "⬡")
    
    def _draw_expanded(self, painter: QPainter, center: QPointF):
        """Draw expanded state with 6 trapezoid segments."""
        inner_r = 38
        outer_r = 100
        
        launchers = self.storage.load_launchers()
        toolbars = launchers.get('toolbars', [])
        
        default_colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
        
        for i in range(6):
            path = self._get_segment_path(i, inner_r, outer_r)
            
            toolbar = toolbars[i] if i < len(toolbars) else None
            
            if toolbar:
                color = QColor(toolbar.get('color', default_colors[i]))
                name = toolbar.get('name', '')
            else:
                color = QColor(60, 70, 85)
                name = "+"
            
            # Dim if petal is open for this segment
            if i in self.open_petals:
                color = color.darker(150)
            elif i == self._hovered_segment:
                color = color.lighter(130)
            
            grad = QLinearGradient(
                center.x(), center.y() - outer_r,
                center.x(), center.y() + outer_r
            )
            grad.setColorAt(0, color.lighter(115))
            grad.setColorAt(1, color.darker(115))
            
            painter.setBrush(QBrush(grad))
            painter.setPen(QPen(color.darker(130), 1.5))
            painter.drawPath(path)
            
            # Draw label
            mid_angle = -math.pi / 2 + i * math.pi / 3
            label_r = (inner_r + outer_r) / 2
            label_x = center.x() + label_r * math.cos(mid_angle)
            label_y = center.y() + label_r * math.sin(mid_angle)
            
            painter.save()
            painter.translate(label_x, label_y)
            
            rotation = math.degrees(mid_angle) + 90
            if 90 < rotation < 270:
                rotation += 180
            painter.rotate(rotation)
            
            painter.setPen(Qt.GlobalColor.white)
            font = QFont("Segoe UI", 9 if toolbar else 14, QFont.Weight.Bold)
            painter.setFont(font)
            
            display_name = name[:8] + ".." if len(name) > 10 else name
            fm = QFontMetrics(font)
            tw = fm.horizontalAdvance(display_name)
            painter.drawText(QRectF(-tw/2, -10, tw, 20), 
                           Qt.AlignmentFlag.AlignCenter, display_name)
            painter.restore()
        
        # Draw center hex
        center_r = 35
        hex_path = self._hex_path(center, center_r)
        
        grad = QRadialGradient(center, center_r)
        grad.setColorAt(0, QColor(55, 65, 85))
        grad.setColorAt(1, QColor(35, 45, 65))
        
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(90, 110, 140), 2))
        painter.drawPath(hex_path)
        
        painter.setPen(QColor(150, 170, 200))
        font = QFont("Segoe UI", 16)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "×")
    
    def _hit_test(self, pos: QPointF) -> str:
        """Determine what was clicked."""
        center = self._get_center()
        dx = pos.x() - center.x()
        dy = pos.y() - center.y()
        dist = math.sqrt(dx*dx + dy*dy)
        
        if self._state == 'collapsed':
            if dist <= 48:
                return 'center'
            return 'none'
        
        elif self._state == 'expanded':
            if dist <= 35:
                return 'center'
            elif dist >= 38 and dist <= 100:
                # Use proper angle calculation for segments
                angle = math.atan2(dy, dx)
                # Convert to 0-2pi range starting from top (-pi/2)
                angle = (angle + math.pi / 2)
                if angle < 0:
                    angle += 2 * math.pi
                angle = angle % (2 * math.pi)
                
                # Each segment is 60 degrees (pi/3)
                segment = int(angle / (math.pi / 3))
                if segment > 5:
                    segment = 5
                return f'segment_{segment}'
            return 'none'
        
        return 'none'
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = QPointF(event.position())
            hit = self._hit_test(pos)
            
            if hit == 'center':
                self._handle_center_click()
            elif hit.startswith('segment_'):
                segment = int(hit.split('_')[1])
                self._handle_segment_click(segment)
            
            event.accept()
    
    def mouseMoveEvent(self, event):
        if self._state == 'expanded':
            pos = QPointF(event.position())
            hit = self._hit_test(pos)
            
            old_hover = self._hovered_segment
            if hit.startswith('segment_'):
                self._hovered_segment = int(hit.split('_')[1])
            else:
                self._hovered_segment = -1
            
            if old_hover != self._hovered_segment:
                self.update()
        
        event.accept()
    
    def leaveEvent(self, event):
        self._hovered_segment = -1
        self.update()
    
    def _handle_center_click(self):
        """Handle click on center hex."""
        if self._state == 'collapsed':
            self._expand()
        elif self._state == 'expanded':
            self._collapse()
    
    def _handle_segment_click(self, segment: int):
        """Handle click on a trapezoid segment - toggle petal."""
        launchers = self.storage.load_launchers()
        toolbars = launchers.get('toolbars', [])
        
        if segment in self.open_petals:
            # Close this petal
            petal = self.open_petals.pop(segment)
            petal.close()
            self.update()
        elif segment < len(toolbars):
            # Open this petal
            toolbar = toolbars[segment]
            self._open_petal(segment, toolbar)
        else:
            # Empty slot - add new toolbar
            self._add_toolbar()
    
    def _open_petal(self, segment: int, toolbar: dict):
        """Open a petal window for a segment."""
        global_center = self._get_global_center()
        petal = PetalWindow(toolbar, segment, global_center)
        petal.show()
        self.open_petals[segment] = petal
        self.update()
        
        # Raise the drag handle to be above petals
        window = self.window()
        if window and hasattr(window, 'drag_handle'):
            window.raise_()
    
    def _expand(self):
        """Expand to show segments - expand from center."""
        old_size = self.size()
        new_size = self._expanded_size
        
        # Calculate position adjustment to keep center fixed
        delta = (new_size - old_size.width()) // 2
        
        self._state = 'expanded'
        self.setFixedSize(new_size, new_size)
        
        # Adjust window position to keep center in place
        window = self.window()
        if window:
            window.move(window.x() - delta, window.y() - delta)
        
        self.update()
    
    def _collapse(self):
        """Collapse to small hex - collapse to center."""
        old_size = self.size()
        new_size = self._collapsed_size
        
        # Close all petals
        for petal in self.open_petals.values():
            petal.close()
        self.open_petals.clear()
        
        # Calculate position adjustment to keep center fixed
        delta = (old_size.width() - new_size) // 2
        
        self._state = 'collapsed'
        self.setFixedSize(new_size, new_size)
        
        # Adjust window position to keep center in place
        window = self.window()
        if window:
            window.move(window.x() + delta, window.y() + delta)
        
        self.update()
    
    def _add_toolbar(self):
        """Add a new toolbar."""
        name, ok = QInputDialog.getText(self, "New Toolbar", "Toolbar name:")
        if ok and name:
            colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"]
            launchers = self.storage.load_launchers()
            idx = len(launchers.get('toolbars', []))
            color = colors[idx % len(colors)]
            self.storage.add_toolbar(name, color)
            self.update()
    
    def contextMenuEvent(self, event):
        # Use pos() instead of position() for QContextMenuEvent
        local_pos = event.pos()
        global_pos = event.globalPos()
        
        menu = QMenu(self)
        
        segment = -1
        toolbar_id = None
        toolbar_name = ""
        
        if self._state == 'expanded':
            pos = QPointF(local_pos.x(), local_pos.y())
            hit = self._hit_test(pos)
            
            if hit.startswith('segment_'):
                segment = int(hit.split('_')[1])
                launchers = self.storage.load_launchers()
                toolbars = launchers.get('toolbars', [])
                
                if segment < len(toolbars):
                    toolbar = toolbars[segment]
                    toolbar_id = toolbar['id']
                    toolbar_name = toolbar.get('name', '')
        
        if toolbar_id is not None:
            # Segment-specific menu
            rename_action = menu.addAction("Rename...")
            
            color_menu = menu.addMenu("Change Color")
            blue_action = color_menu.addAction("Blue")
            red_action = color_menu.addAction("Red")
            green_action = color_menu.addAction("Green")
            orange_action = color_menu.addAction("Orange")
            purple_action = color_menu.addAction("Purple")
            teal_action = color_menu.addAction("Teal")
            
            menu.addSeparator()
            delete_action = menu.addAction("Delete Group")
            
            action = menu.exec(global_pos)
            
            if action == rename_action:
                QTimer.singleShot(50, lambda: self._do_rename(toolbar_id, toolbar_name))
            elif action == delete_action:
                QTimer.singleShot(50, lambda: self._do_delete(segment, toolbar_id))
            elif action == blue_action:
                self._do_color_change(toolbar_id, "#3498db")
            elif action == red_action:
                self._do_color_change(toolbar_id, "#e74c3c")
            elif action == green_action:
                self._do_color_change(toolbar_id, "#2ecc71")
            elif action == orange_action:
                self._do_color_change(toolbar_id, "#f39c12")
            elif action == purple_action:
                self._do_color_change(toolbar_id, "#9b59b6")
            elif action == teal_action:
                self._do_color_change(toolbar_id, "#1abc9c")
        else:
            # Default menu for non-segment areas
            add_action = menu.addAction("Add Group")
            menu.addSeparator()
            close_all_action = menu.addAction("Close All Petals")
            menu.addSeparator()
            hide_action = menu.addAction("Hide Launcher")
            
            action = menu.exec(global_pos)
            
            if action == add_action:
                QTimer.singleShot(50, self._add_toolbar)
            elif action == close_all_action:
                for petal in list(self.open_petals.values()):
                    petal.close()
                self.open_petals.clear()
                self.update()
            elif action == hide_action:
                self.window().hide()
    
    def _do_rename(self, toolbar_id: str, current_name: str):
        """Handle rename dialog separately from context menu."""
        new_name, ok = QInputDialog.getText(
            self, "Rename Group", "New name:", 
            text=current_name)
        if ok and new_name:
            self.storage.rename_toolbar(toolbar_id, new_name)
            self.update()
    
    def _do_delete(self, segment: int, toolbar_id: str):
        """Handle delete separately from context menu."""
        if segment in self.open_petals:
            self.open_petals[segment].close()
            del self.open_petals[segment]
        self.storage.delete_toolbar(toolbar_id)
        self.update()
    
    def _do_color_change(self, toolbar_id: str, color: str):
        """Handle color change."""
        launchers = self.storage.load_launchers()
        for tb in launchers.get('toolbars', []):
            if tb['id'] == toolbar_id:
                tb['color'] = color
                break
        self.storage.save_launchers(launchers)
        self.update()


class DragHandle(QWidget):
    """A visible drag handle bar for moving the launcher, with a close button."""
    
    CLOSE_BTN_SIZE = 14  # diameter of the close button hit area

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(20)
        self.setCursor(Qt.CursorShape.SizeAllCursor)
        self._drag_pos = None
        self._close_hovered = False
        self.setMouseTracking(True)

    def _close_btn_rect(self):
        """Return the rectangle for the close button (right side of handle)."""
        s = self.CLOSE_BTN_SIZE
        x = self.width() - s - 5   # 5px from right edge
        y = (self.height() - s) // 2
        return QRectF(x, y, s, s)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect().adjusted(2, 2, -2, -2)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), 8, 8)
        
        grad = QLinearGradient(0, 0, 0, rect.height())
        grad.setColorAt(0, QColor(70, 80, 100, 220))
        grad.setColorAt(1, QColor(50, 60, 80, 220))
        
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(100, 120, 150), 1))
        painter.drawPath(path)
        
        # Drag dots (centered, shifted slightly left to make room for close btn)
        center_x = self.width() // 2 - 4
        center_y = self.height() // 2
        painter.setBrush(QColor(130, 150, 180))
        painter.setPen(Qt.PenStyle.NoPen)
        
        for offset in [-12, -4, 4, 12]:
            painter.drawEllipse(QPointF(center_x + offset, center_y), 2, 2)

        # Close button "x"
        btn = self._close_btn_rect()
        cx = btn.center().x()
        cy = btn.center().y()

        if self._close_hovered:
            painter.setBrush(QColor(220, 60, 60, 180))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(btn)
            pen_color = QColor(255, 255, 255, 230)
        else:
            pen_color = QColor(160, 170, 190, 180)

        painter.setPen(QPen(pen_color, 1.5))
        d = 3  # half-length of x strokes
        painter.drawLine(QPointF(cx - d, cy - d), QPointF(cx + d, cy + d))
        painter.drawLine(QPointF(cx + d, cy - d), QPointF(cx - d, cy + d))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._close_btn_rect().contains(event.position()):
                # Hide the launcher window
                self.window().hide()
                event.accept()
                return
            self._drag_pos = event.globalPosition().toPoint() - self.window().frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        # Track close button hover
        hovered = self._close_btn_rect().contains(event.position())
        if hovered != self._close_hovered:
            self._close_hovered = hovered
            self.setCursor(Qt.CursorShape.PointingHandCursor if hovered
                           else Qt.CursorShape.SizeAllCursor)
            self.update()

        if self._drag_pos is not None and not hovered:
            self.window().move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = None
            parent = self.window()
            if hasattr(parent, '_save_position'):
                parent._save_position()
            event.accept()


class LauncherWindow(QWidget):
    """Container window for the hex launcher."""
    
    DRAG_HANDLE_HEIGHT = 24
    
    def __init__(self):
        super().__init__()
        self.storage = get_storage()
        
        self._setup_window()
        self._setup_ui()
        self._load_position()
    
    def _setup_window(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    
    def _setup_ui(self):
        self.drag_handle = DragHandle(self)
        self.drag_handle.move(0, 0)
        
        self.launcher = HexLauncherWidget(self)
        self.launcher.move(0, self.DRAG_HANDLE_HEIGHT)
        self._update_size()
        
        self.launcher.installEventFilter(self)
    
    def eventFilter(self, obj, event):
        if obj == self.launcher and event.type() == event.Type.Resize:
            self._update_size()
        return super().eventFilter(obj, event)
    
    def _update_size(self):
        launcher_size = self.launcher.size()
        total_height = launcher_size.height() + self.DRAG_HANDLE_HEIGHT
        self.setFixedSize(launcher_size.width(), total_height)
        self.drag_handle.setFixedWidth(launcher_size.width())
    
    def show_and_raise(self):
        self.show()
        self.raise_()
        self.activateWindow()
    
    def close_all_petals(self):
        """Close all open petal windows."""
        for petal in self.launcher.open_petals.values():
            petal.close()
        self.launcher.open_petals.clear()
    
    def _load_position(self):
        settings = self.storage.load_settings()
        x = settings.get('launcher_x', 200)
        y = settings.get('launcher_y', 200)
        self.move(x, y)
    
    def _save_position(self):
        settings = self.storage.load_settings()
        settings['launcher_x'] = self.x()
        settings['launcher_y'] = self.y()
        self.storage.save_settings(settings)
    
    def closeEvent(self, event):
        event.ignore()
        self._save_position()
        self.launcher._collapse()
        self.hide()
