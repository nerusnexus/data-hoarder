# YtDlpPage_Manage.py
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTreeWidget,
                             QTreeWidgetItem, QPushButton, QInputDialog, QMessageBox, QApplication)
from PySide6.QtCore import Qt
from ui.ui_utils import IconManager
from db_manager import DataManager
import yt_dlp_addChannel

class YtDlpManagePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DataManager()

        self.main_layout = QHBoxLayout(self)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Gerenciar Grupos e Canais")
        self.tree.setStyleSheet("QTreeWidget { background-color: #252525; color: white; border-radius: 5px; }")
        self.main_layout.addWidget(self.tree)

        # Load existing data on startup
        self.load_data()

        # Layout de Botões
        self.btn_layout = QVBoxLayout()

        # Configuração dos botões
        btns = [
            ("Create Group", "create_new_folder", "#2ecc71", self.handle_create_group),
            ("Add Channel", "add_circle", "#3498db", self.handle_add_channel),
            ("Edit", "edit", "#f1c40f", self.handle_edit),
            ("Delete", "delete", "#e74c3c", self.handle_delete)
        ]

        for text, icon, color, func in btns:
            b = QPushButton(text)
            b.setFixedSize(140, 35)
            b.setIcon(IconManager.get_icon(icon, color, 18))
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: {color};
                    border: 1px solid {color};
                    border-radius: 5px;
                    font-weight: bold;
                    text-align: center;
                    padding-left: 0px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: white;
                }}
            """)
            b.clicked.connect(func)
            self.btn_layout.addWidget(b)

        self.btn_layout.addStretch()
        self.main_layout.addLayout(self.btn_layout)

    def load_data(self):
        self.tree.clear()
        groups = self.db.get_groups()
        for g_name in groups:
            item = QTreeWidgetItem(self.tree)
            item.setText(0, g_name)
            item.setIcon(0, IconManager.get_icon("folder", "#f1c40f", 16))

            channels = self.db.get_channels(g_name)
            for ch_name in channels:
                ch_item = QTreeWidgetItem(item)
                ch_item.setText(0, ch_name)
                ch_item.setIcon(0, IconManager.get_icon("subscriptions", "#ff5555", 16))

    def handle_create_group(self):
        name, ok = QInputDialog.getText(self, "Novo Grupo", "Nome do Grupo:")
        if ok and name:
            if self.db.add_group(name):
                item = QTreeWidgetItem(self.tree)
                item.setText(0, name)
                item.setIcon(0, IconManager.get_icon("folder", "#f1c40f", 16))
            else:
                QMessageBox.warning(self, "Erro", "Grupo já existe ou erro na DB.")

    def handle_add_channel(self):
        selected = self.tree.currentItem()
        if not selected or selected.parent():
            QMessageBox.warning(self, "Aviso", "Selecione um Grupo primeiro.")
            return

        url, ok = QInputDialog.getText(self, "Adicionar Canal", "Cole o Link do Canal:")
        if ok and url:
            group_name = selected.text(0)

            # Indicate loading
            QApplication.setOverrideCursor(Qt.WaitCursor)
            self.parent().setWindowTitle("Fetching Data... Please Wait") # Optional visual feedback
            QApplication.processEvents()

            # 1. Fetch Data
            info = yt_dlp_addChannel.fetch_channel_data(url)

            QApplication.restoreOverrideCursor()
            self.parent().setWindowTitle("Data Hoarder") # Reset title

            if info:
                # 2. Add to DB
                if self.db.add_channel(group_name, info):
                    # 3. Add to UI
                    ch_name = info.get('title', info.get('channel', 'Unknown'))
                    ch_item = QTreeWidgetItem(selected)
                    ch_item.setText(0, ch_name)
                    ch_item.setIcon(0, IconManager.get_icon("subscriptions", "#ff5555", 16))
                    selected.setExpanded(True)
                    QMessageBox.information(self, "Sucesso", f"Canal '{ch_name}' adicionado com sucesso!")
                else:
                    QMessageBox.warning(self, "Erro", "Erro ao salvar no banco de dados.")
            else:
                QMessageBox.critical(self, "Erro", "Falha ao obter dados do canal. Verifique o link.")

    def handle_delete(self):
        selected = self.tree.currentItem()
        if not selected: return

        name = selected.text(0)
        is_group = selected.parent() is None
        parent_name = None if is_group else selected.parent().text(0)

        confirm = QMessageBox.question(self, "Confirmar", f"Deletar '{name}'?\nIsso apagará os arquivos fisicamente.")
        if confirm == QMessageBox.Yes:
            self.db.delete_item(name, is_group, parent_name)
            (selected.parent() or self.tree.invisibleRootItem()).removeChild(selected)

    def handle_edit(self):
        selected = self.tree.currentItem()
        if not selected: return

        old_name = selected.text(0)
        is_group = selected.parent() is None
        parent_name = None if is_group else selected.parent().text(0)

        new_name, ok = QInputDialog.getText(self, "Editar", "Novo Nome:", text=old_name)
        if ok and new_name and new_name != old_name:
            self.db.rename_item(old_name, new_name, is_group, parent_name)
            selected.setText(0, new_name)
