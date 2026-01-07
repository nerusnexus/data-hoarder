from PySide6.QtWidgets import QMainWindow, QFrame, QGraphicsDropShadowEffect, QLabel, QWidget, QApplication, QPushButton, QSizePolicy
from PySide6.QtGui import QFontDatabase, QFont, QColor, QIcon, QPixmap, QPainter, QCursor
from PySide6.QtCore import Qt, QPoint, QSize, QPropertyAnimation, QEasingCurve, QTimer
from ui_mainwindow import Ui_MainWindow
import os

# =============================================================================
# CLASSE AUXILIAR: ALÇA DE REDIMENSIONAMENTO (GRIP)
# =============================================================================
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

# =============================================================================
# JANELA PRINCIPAL
# =============================================================================
class DataHoarderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ---------------------------------------------------------
        # CONFIGURAÇÕES
        # ---------------------------------------------------------
        self.sidebar_max_width = 200   # Largura Aberta
        self.sidebar_min_width = 50    # Largura Recolhida (Só ícones)
        self.animation_duration = 200  # Duração (ms)

        self.sidebar_expanded = True
        self.grip_size = 5

        # Trava para evitar cliques múltiplos durante animação
        self.is_animating = False

        # 1. CONFIGURAÇÃO FRAMELESS
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("QMainWindow { background: transparent; }")

        # 2. INICIALIZA GRIPS
        self.side_grips = [
            SideGrip(self, Qt.LeftEdge), SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge), SideGrip(self, Qt.BottomEdge),
        ]
        self.corner_grips = [
            SideGrip(self, "top_left"), SideGrip(self, "top_right"),
            SideGrip(self, "bottom_left"), SideGrip(self, "bottom_right"),
        ]

        # 3. ESTILOS CSS
        self.ui.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-color: #1a1a1a;
                border-radius: 10px;
            }
            QFrame#frame_sidebar {
                background-color: #1a1a1a;
                border-bottom-left-radius: 10px;
                padding-bottom: 10px;
                /* Impede que conteúdo vaze ao encolher */
            }
            QFrame#frame_content, QStackedWidget, QWidget#page, QWidget#page_2 {
                background-color: transparent;
            }

            /* Botões da Sidebar - Base */
            QFrame#frame_sidebar QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
                color: #FFFFFF;
                text-align: left;
                padding: 5px;
                max-height: 50px;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
            }
            QFrame#frame_sidebar QPushButton:hover { background-color: #333333; color: white; }
            QFrame#frame_sidebar QPushButton:checked { background-color: #444444; color: white; }

            /* Botões de Janela */
            QPushButton#btn_close, QPushButton#btn_minimize, QPushButton#btn_maximize {
                background-color: transparent; border: none; border-radius: 10px; color: #cccccc; padding: 5px;
            }
            QPushButton#btn_close:hover { background-color: #ff5555; color: white; }
            QPushButton#btn_minimize:hover { background-color: #333333; color: white; }
            QPushButton#btn_maximize:hover { background-color: #333333; color: white; }

            QLabel#lbl_app_title {
                color: #FFFFFF; font-family: 'Segoe UI'; font-weight: bold; font-size: 14px; padding-left: 10px;
            }
        """)

        # 4. REMOVE BORDAS NATIVAS
        self.ui.frame_title_bar.setFrameShape(QFrame.NoFrame)
        self.ui.frame_content.setFrameShape(QFrame.NoFrame)
        self.ui.frame_sidebar.setFrameShape(QFrame.NoFrame)

        # Adiciona Título
        self.lbl_title = QLabel("Data Hoarder")
        self.lbl_title.setObjectName("lbl_app_title")
        self.ui.horizontalLayout.insertWidget(0, self.lbl_title)

        # Zera Margens
        if self.ui.centralwidget.layout():
            self.ui.centralwidget.layout().setContentsMargins(0, 0, 0, 0)
            self.ui.centralwidget.layout().setSpacing(0)
        if hasattr(self.ui, 'horizontalLayout_2'):
            self.ui.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
            self.ui.horizontalLayout_2.setSpacing(0)

        # SETUP INICIAL DA SIDEBAR
        # Permite encolher até 0
        self.ui.frame_sidebar.setMinimumWidth(0)
        # Define largura máxima inicial
        self.ui.frame_sidebar.setMaximumWidth(self.sidebar_max_width)

        # 5. SOMBRA
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # 6. SETUPS FINAIS
        self.setup_fonts()
        self.setup_floating_button()
        self.setup_sidebar_buttons()
        self.setup_window_buttons()

        self.drag_pos = None

        # Conexões
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_minimize.clicked.connect(self.showMinimized)
        self.ui.btn_maximize.clicked.connect(self.toggle_maximize)
        self.ui.btn_toggle.clicked.connect(self.toggle_sidebar)

    # =========================================================================
    # EVENTOS (RESIZE)
    # =========================================================================
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grips()

        # Mantém a posição Y correta do botão flutuante
        if hasattr(self, 'btn_floating_open'):
            # Margem de 50px do fundo
            y_pos = self.height() - self.btn_floating_open.height() - 50

            # Se o botão estiver visível e na posição final (x>=0), atualiza Y
            if self.btn_floating_open.isVisible() and self.btn_floating_open.x() >= 0:
                self.btn_floating_open.move(0, y_pos)

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
        if hasattr(self, 'btn_floating_open'): self.btn_floating_open.raise_()

    # =========================================================================
    # BOTÃO FLUTUANTE
    # =========================================================================
    def setup_floating_button(self):
        self.btn_floating_open = QPushButton(self.ui.centralwidget)
        self.btn_floating_open.setObjectName("btn_floating_open")
        self.btn_floating_open.setFixedSize(20, 40)
        self.btn_floating_open.setCursor(Qt.PointingHandCursor)
        self.btn_floating_open.hide() # Começa invisível

        self.btn_floating_open.setIcon(self.get_icon("chevron_right", "#cccccc"))
        self.btn_floating_open.setIconSize(QSize(20, 20))

        self.btn_floating_open.setStyleSheet("""
            QPushButton {
                background-color: #252525;
                border-left: none;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
            }
            QPushButton:hover { background-color: #0078d4; }
        """)
        self.btn_floating_open.clicked.connect(self.open_sidebar_from_floating)

    # =========================================================================
    # ÍCONES
    # =========================================================================
    def setup_fonts(self):
        font_path = os.path.join(os.path.dirname(__file__), "MaterialSymbolsRounded-VariableFont_FILL,GRAD,opsz,wght.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            self.icon_font = QFont(font_families[0])
            self.icon_font.setPixelSize(26)
        else:
            self.icon_font = QFont()

    def get_icon(self, identifier, color="#FFFFFF", size=24):
        if identifier.endswith(".svg"):
            path = os.path.join(os.path.dirname(__file__), identifier)
            if os.path.exists(path):
                return QIcon(path)

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        paint_font = QFont(self.icon_font)
        paint_font.setPixelSize(size)
        painter.setFont(paint_font)
        painter.setPen(QColor(color))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, identifier)
        painter.end()
        return QIcon(pixmap)

    # =========================================================================
    # BOTÕES SIDEBAR
    # =========================================================================
    def setup_sidebar_buttons(self):
        self.icon_size = 40

        self.sidebar_btn_data = [
            [self.ui.btn_toggle, "menu", "Menu", None, 5],
            [self.ui.btn_home, "home", "Home", 0, 10],
            [self.ui.btn_library, "library_books", "Library", 1, 5],
            [getattr(self.ui, 'btn_ytdlp', None), "icons/yt-dlp.svg", "Yt-dlp", 2, 5],
            [self.ui.btn_database, "database", "Database", 3, 5],
            [self.ui.btn_settings, "settings", "Settings", 4, 5],
            [self.ui.btn_closeSideTab, "chevron_left", "Close Tab", None, 5]
        ]

        for btn, icon_identifier, label_text, page_index, margin_top in self.sidebar_btn_data:
            if btn and hasattr(self.ui, btn.objectName()):
                # CRÍTICO: Permite encolher ignorando texto
                btn.setMinimumWidth(0)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

                icon = self.get_icon(icon_identifier, color="#cccccc", size=self.icon_size)
                btn.setIcon(icon)
                btn.setIconSize(QSize(self.icon_size, self.icon_size))

                btn.setText(f"  {label_text}")
                btn.setFixedHeight(50)

                # CSS com Padding Fixo (5px) para centralizar ícone quando fechado
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: transparent;
                        border: none;
                        border-radius: 5px;
                        color: #FFFFFF;
                        text-align: left;
                        padding-left: 5px;
                        margin-top: {margin_top}px;
                        font-size: 16px;
                        font-family: 'Segoe UI', sans-serif;
                    }}
                    QPushButton:hover {{ background-color: #333333; color: white; }}
                    QPushButton:checked {{ background-color: #444444; color: white; }}
                """)

                if page_index is not None:
                    btn.setCheckable(True)
                    btn.setAutoExclusive(True)
                    btn.clicked.connect(lambda checked=False, p=page_index: self.ui.stacked_pages.setCurrentIndex(p))

                if btn == self.ui.btn_closeSideTab:
                    btn.clicked.connect(self.close_sidebar_completely)

        if hasattr(self.ui, 'btn_home'): self.ui.btn_home.click()

    def setup_window_buttons(self):
        self.ui.btn_close.setIcon(self.get_icon("close", "#cccccc"))
        self.ui.btn_close.setText("")
        self.ui.btn_minimize.setIcon(self.get_icon("minimize", "#cccccc"))
        self.ui.btn_minimize.setText("")
        self.ui.btn_maximize.setIcon(self.get_icon("check_box_outline_blank", "#cccccc"))
        self.ui.btn_maximize.setText("")

    # =========================================================================
    # LÓGICA DE ANIMAÇÃO COM TRAVA (LOCK)
    # =========================================================================

    def unlock_animation(self):
        """ Destrava o sistema para permitir novos cliques """
        self.is_animating = False

    def toggle_sidebar(self):
        # 1. Verifica Trava
        if self.is_animating: return
        self.is_animating = True

        width_extended = self.sidebar_max_width
        width_collapsed = self.sidebar_min_width

        self.animation = QPropertyAnimation(self.ui.frame_sidebar, b"maximumWidth")
        self.animation.setDuration(self.animation_duration)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        if self.sidebar_expanded:
            self.animation.setStartValue(width_extended)
            self.animation.setEndValue(width_collapsed)
        else:
            self.animation.setStartValue(width_collapsed)
            self.animation.setEndValue(width_extended)

        # Destrava ao terminar
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
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        # Chama a limpeza e a próxima animação
        self.animation.finished.connect(self._on_sidebar_closed)

        self.animation.start()
        self.sidebar_expanded = False

    def _on_sidebar_closed(self):
        """ Limpa o frame da tela para evitar artefatos e chama botão flutuante """
        self.ui.frame_sidebar.hide()
        self.show_floating_button_animated()

    def show_floating_button_animated(self):
        # Posição Y (50px margem inferior)
        y_pos = self.height() - self.btn_floating_open.height() - 10

        start_pos = QPoint(-self.btn_floating_open.width(), y_pos)
        end_pos = QPoint(0, y_pos)

        self.btn_floating_open.move(start_pos)
        self.btn_floating_open.show()

        self.anim_btn = QPropertyAnimation(self.btn_floating_open, b"pos")
        self.anim_btn.setDuration(300)
        self.anim_btn.setStartValue(start_pos)
        self.anim_btn.setEndValue(end_pos)
        self.anim_btn.setEasingCurve(QEasingCurve.OutCubic)

        # Só destrava tudo aqui
        self.anim_btn.finished.connect(self.unlock_animation)
        self.anim_btn.start()

    def open_sidebar_from_floating(self):
        if self.is_animating: return
        self.is_animating = True

        self.btn_floating_open.hide()

        # Mostra o frame antes de animar
        self.ui.frame_sidebar.show()
        self.ui.frame_sidebar.raise_()

        self.animation = QPropertyAnimation(self.ui.frame_sidebar, b"maximumWidth")
        self.animation.setDuration(self.animation_duration)
        self.animation.setStartValue(0)
        self.animation.setEndValue(self.sidebar_max_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)

        self.animation.finished.connect(self.unlock_animation)
        self.animation.start()

        self.sidebar_expanded = True

    # =========================================================================
    # EVENTOS MOUSE
    # =========================================================================
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self.ui, 'frame_title_bar') and self.ui.frame_title_bar.underMouse():
                self.toggle_maximize()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if hasattr(self.ui, 'frame_title_bar') and self.ui.frame_title_bar.underMouse():
                self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos is not None:
            if self.isMaximized():
                screen_width = self.width()
                mouse_x_ratio = event.position().x() / screen_width
                self.showNormal()
                self.ui.btn_maximize.setIcon(self.get_icon("check_box_outline_blank", "#cccccc"))
                self.ui.btn_maximize.setText("")
                self.ui.centralwidget.setStyleSheet(self.ui.centralwidget.styleSheet().replace("border-radius: 0px;", "border-radius: 12px;"))
                new_width = self.width()
                adjusted_x = event.globalPosition().x() - (new_width * mouse_x_ratio)
                self.move(int(adjusted_x), int(event.globalPosition().y()) - 10)
                self.drag_pos = event.globalPosition().toPoint()
            else:
                delta = QPoint(event.globalPosition().toPoint() - self.drag_pos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.centralwidget.setStyleSheet(self.ui.centralwidget.styleSheet().replace("border-radius: 0px;", "border-radius: 12px;"))
            self.ui.btn_maximize.setIcon(self.get_icon("check_box_outline_blank", "#cccccc"))
        else:
            self.showMaximized()
            self.ui.centralwidget.setStyleSheet(self.ui.centralwidget.styleSheet().replace("border-radius: 12px;", "border-radius: 0px;"))
            self.ui.btn_maximize.setIcon(self.get_icon("filter_none", "#cccccc"))
