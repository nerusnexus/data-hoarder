from PySide6.QtWidgets import QMainWindow, QFrame, QGraphicsDropShadowEffect, QLabel, QWidget, QPushButton, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QColor, QIcon, QPixmap, QPainter
from PySide6.QtCore import Qt, QPoint, QSize, QPropertyAnimation, QEasingCurve
from ui_mainwindow import Ui_MainWindow
import os

# Importações dos seus módulos customizados na pasta 'ui'
from ui.custom_widgets import SideGrip
from ui.StyleSheets import MAIN_STYLE_SHEET, FLOATING_OPEN_BUTTON, SIDEBAR_BUTTON_MARGIN
from ui.ui_utils import IconManager  # Centraliza o uso do .ttf
from YtDlpPage import YtDlpPage

# Se você já criou o core/manager.py, importe-o aqui
# from core.manager import DataManager

class DataHoarderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 1. ATRIBUTOS E CONFIGURAÇÕES
        self.sidebar_max_width = 200
        self.sidebar_min_width = 50
        self.animation_duration = 200
        self.sidebar_expanded = True
        self.grip_size = 5
        self.is_animating = False
        self.drag_pos = None

        # Inicializa o gerenciador de dados (SQL e Pastas)
        # self.data_manager = DataManager()

        # 2. CONFIGURAÇÃO FRAMELESS
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("QMainWindow { background: transparent; }")

        # 3. INICIALIZA GRIPS E ESTILOS GLOBAIS
        self.setup_grips()
        self.ui.centralwidget.setStyleSheet(MAIN_STYLE_SHEET)

        # 4. CUSTOMIZAÇÃO DA INTERFACE (Bordas, Títulos, Margens)
        self.setup_ui_visuals()

        # 5. SETUPS DE COMPONENTES
        self.setup_floating_button()
        self.setup_sidebar_buttons()
        self.setup_window_buttons()
        self.setup_pages()

        # 6. CONEXÕES DE BOTÕES DE JANELA
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_minimize.clicked.connect(self.showMinimized)
        self.ui.btn_maximize.clicked.connect(self.toggle_maximize)
        self.ui.btn_toggle.clicked.connect(self.toggle_sidebar)

    def setup_grips(self):
        """Inicializa as alças de redimensionamento importadas de custom_widgets.py"""
        self.side_grips = [
            SideGrip(self, Qt.LeftEdge), SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge), SideGrip(self, Qt.BottomEdge),
        ]
        self.corner_grips = [
            SideGrip(self, "top_left"), SideGrip(self, "top_right"),
            SideGrip(self, "bottom_left"), SideGrip(self, "bottom_right"),
        ]

    def setup_ui_visuals(self):
        """Limpa bordas do Qt Designer e adiciona sombra/título"""
        self.ui.frame_title_bar.setFrameShape(QFrame.NoFrame)
        self.ui.frame_content.setFrameShape(QFrame.NoFrame)
        self.ui.frame_sidebar.setFrameShape(QFrame.NoFrame)

        self.lbl_title = QLabel("Data Hoarder")
        self.lbl_title.setObjectName("lbl_app_title")
        self.ui.horizontalLayout.insertWidget(0, self.lbl_title)

        if self.ui.centralwidget.layout():
            self.ui.centralwidget.layout().setContentsMargins(0, 0, 0, 0)
            self.ui.centralwidget.layout().setSpacing(0)

        self.ui.frame_sidebar.setMinimumWidth(0)
        self.ui.frame_sidebar.setMaximumWidth(self.sidebar_max_width)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

    def setup_pages(self):
        """Injeta a página modular do YT-DLP"""
        self.ytdlp_content = YtDlpPage()
        layout = QVBoxLayout(self.ui.page_ytdlp)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.ytdlp_content)

    def setup_sidebar_buttons(self):
        """Configura ícones, textos e estilos dinâmicos da sidebar"""
        self.icon_size = 40
        self.sidebar_btn_data = [
            [self.ui.btn_toggle, "menu", "Menu", None, 5],
            [self.ui.btn_home, "home", "Home", 0, 10],
            [self.ui.btn_library, "library_books", "Library", 1, 5],
            [getattr(self.ui, 'btn_ytdlp', None), "icons/yt-dlp.svg", "Yt-dlp", 2, 5],
            [self.ui.btn_database, "database", "Database", 3, 5],
            [self.ui.btn_settings, "settings", "Settings", 4, 5],
            [self.ui.btn_info, "info", "Info", 5, 5],
            [self.ui.btn_closeSideTab, "chevron_left", "Close Tab", None, 5]
        ]

        for btn, icon_id, label, page_idx, margin_top in self.sidebar_btn_data:
            if btn and hasattr(self.ui, btn.objectName()):
                btn.setMinimumWidth(0)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                # Usa o IconManager para pegar ícones do seu .ttf ou .svg
                icon = IconManager.get_icon(icon_id, color="#cccccc", size=self.icon_size)
                btn.setIcon(icon)
                btn.setIconSize(QSize(self.icon_size, self.icon_size))
                btn.setText(f"  {label}")
                btn.setFixedHeight(50)

                # Aplica apenas a margem dinâmica (preserva o visual global do MAIN_STYLE_SHEET)
                btn.setStyleSheet(SIDEBAR_BUTTON_MARGIN.format(margin_top))

                if page_idx is not None:
                    btn.setCheckable(True)
                    btn.setAutoExclusive(True)
                    btn.clicked.connect(lambda checked=False, p=page_idx: self.ui.stacked_pages.setCurrentIndex(p))

                if btn == self.ui.btn_closeSideTab:
                    btn.clicked.connect(self.close_sidebar_completely)

        if hasattr(self.ui, 'btn_home'): self.ui.btn_home.click()

    def setup_window_buttons(self):
        # Close
        self.ui.btn_close.setIcon(IconManager.get_icon("close", "#cccccc", 18))
        self.ui.btn_close.setText("") # Garante que não tem texto

        # Minimize
        self.ui.btn_minimize.setIcon(IconManager.get_icon("minimize", "#cccccc", 18))
        self.ui.btn_minimize.setText("")

        # Maximize
        self.ui.btn_maximize.setIcon(IconManager.get_icon("check_box_outline_blank", "#cccccc", 18))
        self.ui.btn_maximize.setText("")

    def setup_floating_button(self):
        self.btn_floating_open = QPushButton(self.ui.centralwidget)
        self.btn_floating_open.setFixedSize(20, 40)
        self.btn_floating_open.setCursor(Qt.PointingHandCursor)
        self.btn_floating_open.hide()
        self.btn_floating_open.setIcon(IconManager.get_icon("chevron_right", "#cccccc", 20))
        self.btn_floating_open.setStyleSheet(FLOATING_OPEN_BUTTON)
        self.btn_floating_open.clicked.connect(self.open_sidebar_from_floating)

    # --- LÓGICA DE ANIMAÇÃO E EVENTOS DE MOUSE ---
    # (Mantenha os métodos toggle_sidebar, resizeEvent, update_grips, mouseMoveEvent etc. como estavam na sua versão anterior, pois eles controlam o comportamento da janela)

    def unlock_animation(self): self.is_animating = False

    def toggle_sidebar(self):
        if self.is_animating: return
        self.is_animating = True
        width_ext, width_col = self.sidebar_max_width, self.sidebar_min_width
        self.animation = QPropertyAnimation(self.ui.frame_sidebar, b"maximumWidth")
        self.animation.setDuration(self.animation_duration)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.setStartValue(width_ext if self.sidebar_expanded else width_col)
        self.animation.setEndValue(width_col if self.sidebar_expanded else width_ext)
        self.animation.finished.connect(self.unlock_animation)
        self.animation.start()
        self.sidebar_expanded = not self.sidebar_expanded

    def close_sidebar_completely(self):
        if self.is_animating: return
        self.is_animating = True
        self.animation = QPropertyAnimation(self.ui.frame_sidebar, b"maximumWidth")
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(self.ui.frame_sidebar.width())
        self.animation.setEndValue(0)
        self.animation.finished.connect(self._on_sidebar_closed)
        self.animation.start()
        self.sidebar_expanded = False

    def _on_sidebar_closed(self):
        self.ui.frame_sidebar.hide()
        self.show_floating_button_animated()

    def show_floating_button_animated(self):
        y_pos = self.height() - self.btn_floating_open.height() - 10
        start, end = QPoint(-self.btn_floating_open.width(), y_pos), QPoint(0, y_pos)
        self.btn_floating_open.move(start)
        self.btn_floating_open.show()
        self.anim_btn = QPropertyAnimation(self.btn_floating_open, b"pos")
        self.anim_btn.setDuration(300)
        self.anim_btn.setStartValue(start)
        self.anim_btn.setEndValue(end)
        self.anim_btn.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_btn.finished.connect(self.unlock_animation)
        self.anim_btn.start()

    def open_sidebar_from_floating(self):
        if self.is_animating: return
        self.is_animating = True
        self.btn_floating_open.hide()
        self.ui.frame_sidebar.show()
        self.animation = QPropertyAnimation(self.ui.frame_sidebar, b"maximumWidth")
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.sidebar_max_width)
        self.animation.finished.connect(self.unlock_animation)
        self.animation.start()
        self.sidebar_expanded = True

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grips()

    def update_grips(self):
        rect = self.rect()
        self.side_grips[0].setGeometry(0, self.grip_size, self.grip_size, rect.height() - 2*self.grip_size)
        self.side_grips[1].setGeometry(self.grip_size, 0, rect.width() - 2*self.grip_size, self.grip_size)
        self.side_grips[2].setGeometry(rect.width() - self.grip_size, self.grip_size, self.grip_size, rect.height() - 2*self.grip_size)
        self.side_grips[3].setGeometry(self.grip_size, rect.height() - self.grip_size, rect.width() - 2*self.grip_size, self.grip_size)
        self.corner_grips[0].setGeometry(0, 0, self.grip_size, self.grip_size)
        self.corner_grips[1].setGeometry(rect.width() - self.grip_size, 0, self.grip_size, self.grip_size)
        self.corner_grips[2].setGeometry(0, rect.height() - self.grip_size, self.grip_size, self.grip_size)
        self.corner_grips[3].setGeometry(rect.width() - self.grip_size, rect.height() - self.grip_size, self.grip_size, self.grip_size)
        for grip in self.side_grips + self.corner_grips: grip.raise_()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and hasattr(self.ui, 'frame_title_bar') and self.ui.frame_title_bar.underMouse():
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            delta = QPoint(event.globalPosition().toPoint() - self.drag_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event): self.drag_pos = None

    def toggle_maximize(self):
        if self.isMaximized(): self.showNormal()
        else: self.showMaximized()
