import os
from PySide6.QtGui import QFont, QFontDatabase, QPixmap, QPainter, QColor, QIcon
from PySide6.QtCore import Qt

class IconManager:
    _icon_font = None

    @classmethod
    def setup_font(cls):
        if cls._icon_font is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(current_dir)
            font_path = os.path.join(root_dir, "MaterialSymbolsRounded-VariableFont_FILL,GRAD,opsz,wght.ttf")
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                cls._icon_font = QFont(family)
            else:
                cls._icon_font = QFont()

    @classmethod
    def get_icon(cls, identifier, color="#FFFFFF", size=24):
        cls.setup_font()
        if identifier.endswith(".svg"):
            current_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(current_dir)
            path = os.path.normpath(os.path.join(root_dir, identifier))
            if os.path.exists(path): return QIcon(path)

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        font = QFont(cls._icon_font)
        font.setPixelSize(size)
        painter.setFont(font)
        painter.setPen(QColor(color))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, identifier)
        painter.end()
        return QIcon(pixmap)
