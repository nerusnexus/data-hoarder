from PySide6.QtWidgets import QMainWindow, QFrame, QGraphicsDropShadowEffect, QLabel, QWidget, QApplication, QHBoxLayout, QVBoxLayout, QSizeGrip
from PySide6.QtGui import QFontDatabase, QFont, QColor, QIcon, QPixmap, QPainter, QCursor, QWindow
from PySide6.QtCore import Qt, QPoint, QSize, QPropertyAnimation, QEasingCurve, QEvent, QRect
from ui_mainwindow import Ui_MainWindow
import os

# =============================================================================
# CLASSE AUXILIAR: ALÇA DE REDIMENSIONAMENTO (GRIP)
# =============================================================================
class SideGrip(QWidget):
    """
    Um widget invisível que fica nas bordas para capturar o mouse e redimensionar.
    """
    def __init__(self, parent, edge):
        super().__init__(parent)
        self.edge = edge
        self.parent_window = parent
        self.setMouseTracking(True)

        # Define o cursor baseado na posição da alça
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
            # Inicia o redimensionamento nativo do sistema (se disponível) ou manual
            self.parent_window.windowHandle().startSystemResize(self.convert_edge(self.edge))

    def convert_edge(self, edge):
        # Converte nossas strings/constantes para as bordas do Qt Window System
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

        # Variáveis
        self.sidebar_expanded = True
        self.grip_size = 5 # Tamanho da borda invisível (aumente se achar difícil clicar)

        # 1. CONFIGURAÇÃO FRAMELESS
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("QMainWindow { background: transparent; }")

        # 2. INICIALIZA AS ALÇAS DE REDIMENSIONAMENTO (GRIPS)
        # Criamos 4 lados + 4 cantos
        self.side_grips = [
            SideGrip(self, Qt.LeftEdge),
            SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge),
            SideGrip(self, Qt.BottomEdge),
        ]
        self.corner_grips = [
            SideGrip(self, "top_left"),
            SideGrip(self, "top_right"),
            SideGrip(self, "bottom_left"),
            SideGrip(self, "bottom_right"),
        ]

        # 3. ESTILOS CSS (Mantendo os seus ajustes visuais)
        self.ui.centralwidget.setStyleSheet("""
            QWidget#centralwidget {
                background-color: #1a1a1a;
                border-radius: 12px;
                /* Borda subtil para destacar do fundo */
            }
            QFrame#frame_sidebar {
                background-color: #1a1a1a;
                border-bottom-left-radius: 12px;
                padding-bottom: 10px;
            }
            /* O conteúdo deve ser transparente para não cobrir o arredondado */
            QFrame#frame_content, QStackedWidget, QWidget#page, QWidget#page_2 {
                background-color: transparent;
            }

            /* Botões da Sidebar */
            QFrame#frame_sidebar QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
                color: #FFFFFF;
                text-align: left;
                padding: 5px;
                max-height: 30px;
                margin-left: 0px;
                margin-right: 0px;
                font-size: 16px;
                font-family: 'Segoe UI', sans-serif;
            }
            QFrame#frame_sidebar QPushButton:hover { background-color: #333333; color: white; }
            QFrame#frame_sidebar QPushButton:checked { background-color: #444444; color: white; }

            /* Botões de Janela */
            QPushButton#btn_close, QPushButton#btn_minimize, QPushButton#btn_maximize {
                background-color: transparent; border: none; border-radius: 10px; color: #cccccc; padding: 2px;
            }
            QPushButton#btn_close:hover { background-color: #ff5555; color: white; }
            QPushButton#btn_minimize:hover { background-color: #333333; color: white; }
            QPushButton#btn_maximize:hover { background-color: #333333; color: white; }

            QLabel#lbl_app_title {
                color: #FFFFFF; font-family: 'Segoe UI'; font-weight: bold; font-size: 14px; padding-left: 10px;
            }
        """)

        # 4. REMOVE BORDAS NATIVAS DOS FRAMES
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

        # Sidebar Limits
        self.sidebar_max_width = 200
        self.sidebar_min_width = 0
        self.ui.frame_sidebar.setMaximumWidth(self.sidebar_max_width)
        self.ui.frame_sidebar.setMinimumWidth(self.sidebar_min_width)

        # 5. SOMBRA
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # 6. SETUPS FINAIS
        self.setup_fonts()
        self.setup_sidebar_buttons()
        self.setup_window_buttons()
        self.setup_navigation()
        self.drag_pos = None

        # Conexões
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_minimize.clicked.connect(self.showMinimized)
        self.ui.btn_maximize.clicked.connect(self.toggle_maximize)
        self.ui.btn_toggle.clicked.connect(self.toggle_sidebar)

    # =========================================================================
    # EVENTO DE REDIMENSIONAMENTO (ATUALIZA POSIÇÃO DAS ALÇAS)
    # =========================================================================
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_grips()

    def update_grips(self):
        rect = self.rect()
        # Define a geometria das alças invisíveis para cobrir as bordas
        # Topo, Baixo, Esquerda, Direita
        self.side_grips[0].setGeometry(0, self.grip_size, self.grip_size, rect.height() - 2*self.grip_size) # Left
        self.side_grips[1].setGeometry(self.grip_size, 0, rect.width() - 2*self.grip_size, self.grip_size) # Top
        self.side_grips[2].setGeometry(rect.width() - self.grip_size, self.grip_size, self.grip_size, rect.height() - 2*self.grip_size) # Right
        self.side_grips[3].setGeometry(self.grip_size, rect.height() - self.grip_size, rect.width() - 2*self.grip_size, self.grip_size) # Bottom

        # Cantos
        self.corner_grips[0].setGeometry(0, 0, self.grip_size, self.grip_size) # Top Left
        self.corner_grips[1].setGeometry(rect.width() - self.grip_size, 0, self.grip_size, self.grip_size) # Top Right
        self.corner_grips[2].setGeometry(0, rect.height() - self.grip_size, self.grip_size, self.grip_size) # Bottom Left
        self.corner_grips[3].setGeometry(rect.width() - self.grip_size, rect.height() - self.grip_size, self.grip_size, self.grip_size)

        # GARANTE QUE AS ALÇAS FIQUEM ACIMA DE TUDO
        for grip in self.side_grips + self.corner_grips:
            grip.raise_()

    # =========================================================================
    # LÓGICA DE ÍCONES E UI
    # =========================================================================
    def setup_fonts(self):
        font_filename = "MaterialSymbolsRounded-VariableFont_FILL,GRAD,opsz,wght.ttf"
        font_path = os.path.join(os.path.dirname(__file__), font_filename)
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            self.icon_font = QFont(font_families[0])
            self.icon_font.setPixelSize(26)
        else:
            self.icon_font = QFont()

    def create_icon_from_font(self, icon_name, color="#FFFFFF", size=24):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        paint_font = QFont(self.icon_font)
        paint_font.setPixelSize(size)
        painter.setFont(paint_font)
        painter.setPen(QColor(color))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, icon_name)
        painter.end()
        return QIcon(pixmap)

    # ---------------------------------------------------------
    # 1. SETUP DOS BOTÕES (Agora guardamos os dados numa lista)
    # ---------------------------------------------------------
    def setup_sidebar_buttons(self):
        icon_size = 38

        # Guardamos os dados numa variável da classe para usar depois no Toggle
        # Formato: [Botão, NomeIcone, TextoLabel]
        self.sidebar_btn_data = [
            [self.ui.btn_toggle, "menu", "Menu"],
            [self.ui.btn_home, "home", "Home"],
            [self.ui.btn_library, "library_books", "Library"],
            [self.ui.btn_settings, "settings", "Settings"],
            [self.ui.btn_database, "database", "Database"],
            [self.ui.btn_closeSideTab, "chevron_left", "Close Side Tab"]
        ]

        for btn, icon_name, label_text in self.sidebar_btn_data:
            if hasattr(self.ui, btn.objectName()):
                icon = self.create_icon_from_font(icon_name, color="#cccccc", size=icon_size)
                btn.setIcon(icon)
                btn.setIconSize(QSize(icon_size, icon_size))

                # Configuração inicial (Barra Aberta)
                btn.setText(f"  {label_text}")
                # Adiciona Tooltip para quando estiver fechado o usuário saber o que é
                btn.setToolTip(label_text)


    def setup_window_buttons(self):
        self.ui.btn_close.setFont(self.icon_font)
        self.ui.btn_close.setText("close")
        self.ui.btn_minimize.setFont(self.icon_font)
        self.ui.btn_minimize.setText("minimize")
        self.ui.btn_maximize.setFont(self.icon_font)
        self.ui.btn_maximize.setText("check_box_outline_blank")

    def setup_navigation(self):
        self.ui.btn_home.setCheckable(True)
        self.ui.btn_library.setCheckable(True)
        self.ui.btn_settings.setCheckable(True)
        self.ui.btn_home.setAutoExclusive(True)
        self.ui.btn_library.setAutoExclusive(True)
        self.ui.btn_settings.setAutoExclusive(True)

        self.ui.btn_home.clicked.connect(lambda: self.ui.stacked_pages.setCurrentIndex(0))
        self.ui.btn_library.clicked.connect(lambda: self.ui.stacked_pages.setCurrentIndex(1))
        self.ui.btn_settings.clicked.connect(lambda: self.ui.stacked_pages.setCurrentIndex(0))
        self.ui.btn_home.click()

    def toggle_sidebar(self):
        width_extended = self.sidebar_max_width
        width_collapsed = 50

        if self.sidebar_expanded:
            start_val = width_extended
            end_val = width_collapsed
        else:
            start_val = width_collapsed
            end_val = width_extended

        self.sidebar_expanded = not self.sidebar_expanded

        self.animation = QPropertyAnimation(self.ui.frame_sidebar, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(start_val)
        self.animation.setEndValue(end_val)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    # =========================================================================
    # EVENTOS DE ARRASTAR E CLICK
    # =========================================================================
    def mouseDoubleClickEvent(self, event):
        # Maximiza ao clicar duas vezes na barra de título
        if event.button() == Qt.LeftButton:
            if hasattr(self.ui, 'frame_title_bar') and self.ui.frame_title_bar.underMouse():
                self.toggle_maximize()

    def mousePressEvent(self, event):
        # Arrasta a janela se clicar na barra de título
        if event.button() == Qt.LeftButton:
            if hasattr(self.ui, 'frame_title_bar') and self.ui.frame_title_bar.underMouse():
                self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        # Lógica de arrastar a janela (Move)
        if self.drag_pos is not None:
            if self.isMaximized():
                screen_width = self.width()
                mouse_x_ratio = event.position().x() / screen_width
                self.showNormal()
                self.ui.btn_maximize.setText("check_box_outline_blank")
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
            self.ui.btn_maximize.setText("check_box_outline_blank")
        else:
            self.showMaximized()
            self.ui.centralwidget.setStyleSheet(self.ui.centralwidget.styleSheet().replace("border-radius: 12px;", "border-radius: 0px;"))
            self.ui.btn_maximize.setText("filter_none")
