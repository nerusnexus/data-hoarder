from PySide6.QtWidgets import QMainWindow
from ui_design import Ui_MainWindow  # Aqui ele puxa o arquivo que você criou no terminal

class DataHoarderGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # Cria o objeto da interface
        self.ui.setupUi(self)      # Monta tudo na tela

        # Teste rápido: vamos mudar o título da janela via código
        self.setWindowTitle("Data Hoarder - Interface Teste")
