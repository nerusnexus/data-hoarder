from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFileDialog, QGroupBox)
from PySide6.QtCore import Qt
from config_manager import ConfigManager

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)

        # -- General Settings Group --
        group_box = QGroupBox("General Configuration")
        group_layout = QVBoxLayout()

        # Label
        lbl_info = QLabel("Root Directory (Where all metadata/files will be stored):")
        group_layout.addWidget(lbl_info)

        # Path Selection Row
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setText(ConfigManager.get_root_path())
        self.path_input.setStyleSheet("padding: 5px; color: #fff; background: #333; border: 1px solid #555;")

        btn_browse = QPushButton("Browse...")
        btn_browse.setCursor(Qt.PointingHandCursor)
        btn_browse.setFixedSize(100, 30)
        btn_browse.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; border-radius: 4px; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_browse.clicked.connect(self.select_folder)

        path_layout.addWidget(self.path_input)
        path_layout.addWidget(btn_browse)

        group_layout.addLayout(path_layout)
        group_box.setLayout(group_layout)

        # Style the Group Box
        group_box.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #555;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px;
            }
        """)

        self.layout.addWidget(group_box)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Root Directory")
        if folder:
            self.path_input.setText(folder)
            ConfigManager.set_root_path(folder)
            # Optional: Notify user or restart prompt could go here
