from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from ui.StyleSheets import YtDlp_PAGE
from SettingsPage_Manage import SettingsManagePage

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)

        # 2. Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setObjectName("settings_tabs")

        # 3. Create Tabs
        # 'General' tab content comes from SettingsPage_Manage.py
        self.tab_general = SettingsManagePage()

        # You can add more tabs here later (e.g., self.tab_advanced = QWidget())

        # 4. Add Tabs
        self.tabs.addTab(self.tab_general, "General")

        # Add to layout
        self.layout.addWidget(self.tabs)

        # Apply Styles
        self.setup_style()

    def setup_style(self):
        self.tabs.setStyleSheet(YtDlp_PAGE)
