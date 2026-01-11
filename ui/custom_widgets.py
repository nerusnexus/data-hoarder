from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from ui.ui_utils import IconManager
from PySide6.QtGui import QCursor


# Border grip to resize window
class SideGrip(QWidget):
    def __init__(self, parent, edge):
        super().__init__(parent)
        self.edge = edge
        self.parent_window = parent
        self.setMouseTracking(True)

        if edge == Qt.LeftEdge or edge == Qt.RightEdge:
            self.setCursor(Qt.SizeHorCursor)
        elif edge == Qt.TopEdge or edge == Qt.BottomEdge:
            self.setCursor(Qt.SizeVerCursor)
        elif edge == "top_left" or edge == "bottom_right":
            self.setCursor(Qt.SizeFDiagCursor)
        elif edge == "top_right" or edge == "bottom_left":
            self.setCursor(Qt.SizeBDiagCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent_window.windowHandle().startSystemResize(self.convert_edge(self.edge))

    def convert_edge(self, edge):
        if edge == Qt.LeftEdge: return Qt.LeftEdge
        if edge == Qt.RightEdge: return Qt.RightEdge
        if edge == Qt.TopEdge: return Qt.TopEdge
        if edge == Qt.BottomEdge: return Qt.BottomEdge
        if edge == "top_left": return Qt.TopEdge | Qt.LeftEdge
        if edge == "top_right": return Qt.TopEdge | Qt.RightEdge
        if edge == "bottom_left": return Qt.BottomEdge | Qt.LeftEdge
        if edge == "bottom_right": return Qt.BottomEdge | Qt.RightEdge
        return edge
