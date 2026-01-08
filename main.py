import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Création de l'application Qt
    # QApplication est obligatoire pour toute application PyQt
    app = QApplication(sys.argv)

    # Création de la fenêtre principale de l'application
    window = MainWindow()

    # Affichage de la fenêtre principale à l'écran
    window.show()

    # Lancement de la boucle principale de l'application
    # sys.exit permet de retourner correctement le code de sortie
    sys.exit(app.exec())

# Point d'entrée du programme
# Cette condition garantit que main() est exécuté uniquement
# lorsque ce fichier est lancé directement
if __name__ == "__main__":
    main()