from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import Qt, QPoint # Adicionamos QPoint para o movimento
from ui_mainwindow import Ui_MainWindow

class DataHoarderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Zerando as margens do layout principal (remove o espaço entre a barra e a borda)
        if self.ui.centralwidget.layout():
            self.ui.centralwidget.layout().setContentsMargins(0, 0, 0, 0)
            self.ui.centralwidget.layout().setSpacing(0)

        # 1. REMOVE BORDAS E DEIXA A JANELA "LISA"
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Variável para rastrear o movimento do mouse para arrastar a janela
        self.old_pos = None

        # 2. CONECTA OS BOTÕES DE CONTROLE DA JANELA
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_minimize.clicked.connect(self.showMinimized)
        self.ui.btn_maximize.clicked.connect(self.alternar_maximizacao)

        # 3. IMPLEMENTAÇÃO DOS ÍCONES (Sua lógica anterior expandida)
        self.configurar_icones()

    def configurar_icones(self):
        font_path = "MaterialSymbolsRounded.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            self.icon_font = QFont(font_families[0])
            self.icon_font.setPixelSize(20) # Tamanho padrão para ícones

            # Ícones da Barra Lateral
            self.aplicar_icone(self.ui.btn_home, "home")
            self.aplicar_icone(self.ui.btn_library, "library_books")
            self.aplicar_icone(self.ui.btn_settings, "settings")
            self.aplicar_icone(self.ui.btn_toggle, "menu")

            # Ícones da Barra de Título (Novos!)
            self.aplicar_icone(self.ui.btn_close, "close")
            self.aplicar_icone(self.ui.btn_minimize, "minimize")
            self.aplicar_icone(self.ui.btn_maximize, "check_box_outline_blank")
        else:
            print(f"Erro ao carregar fonte em {font_path}")

    def aplicar_icone(self, botao, nome_icone):
        """Função auxiliar para aplicar fonte e texto de ligatura"""
        botao.setFont(self.icon_font)
        botao.setText(nome_icone)

    # --- LÓGICA PARA ARRASTAR A JANELA PELA TITLE BAR ---

    def mousePressEvent(self, event):
        # Só permite arrastar se clicar com o botão esquerdo no frame_title_bar
        if event.button() == Qt.LeftButton and self.ui.frame_title_bar.underMouse():
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = QPoint(event.globalPosition().toPoint() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # --- LÓGICA DE MAXIMIZAÇÃO ---

    def alternar_maximizacao(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.btn_maximize.setText("check_box_outline_blank") # Ícone de quadrado
        else:
            self.showMaximized()
            self.ui.btn_maximize.setText("restore") # Ícone de restaurar
