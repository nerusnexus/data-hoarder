import sys
from PySide6.QtWidgets import QApplication
from GUI import DataHoarderGUI  # Importa a classe que criamos no seu arquivo GUI.py

def main():
    # 1. Cria a instância da aplicação (necessário para qualquer app PySide6)
    app = QApplication(sys.argv)

    # 2. Instancia a sua janela personalizada
    # Note que chamamos a classe 'DataHoarderGUI' que está dentro do arquivo GUI.py
    window = DataHoarderGUI()

    # 3. Exibe a janela na tela
    window.show()

    # 4. Inicia o loop de eventos (faz o programa ficar aberto esperando seus cliques)
    sys.exit(app.exec())

# Esta linha garante que o programa só rode se você clicar no 'Play' deste arquivo
if __name__ == "__main__":
    main()
