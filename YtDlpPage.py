from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget, QStackedWidget
from PySide6.QtCore import Qt
from ui.StyleSheets import YtDlp_PAGE
from YtDlpPage_Manage import YtDlpManagePage

class YtDlpPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Layout principal da página
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # 2. Cria o Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setObjectName("ytdlp_tabs")

        # 3. Criar os widgets que serão as abas
        self.tab_subscriptons = QWidget()
        self.tab_playlists = QWidget()
        self.tab_manage = YtDlpManagePage()
        self.tab_config = QWidget()

        # 4. Adicionar as abas ao widget
        self.tabs.addTab(self.tab_subscriptons, "Subscriptions")
        self.tabs.addTab(self.tab_playlists, "Playlists")
        self.tabs.addTab(self.tab_manage, "Manage")
        self.tabs.addTab(self.tab_config, "Config")

        # Adiciona o Tab Widget ao layout da página
        self.layout.addWidget(self.tabs)

        # Aplicar estilo escuro (QSS)
        self.setup_style()

    def setup_style(self):
        self.tabs.setStyleSheet(YtDlp_PAGE)
