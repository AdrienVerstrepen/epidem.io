import sys
import random
from PySide6.QtWidgets import *

class Fenetre(QWidget):
    def __init__(self, son_titre, x, y, son_label, son_bouton):
        super().__init__()
        self.resize(x, y)
        self.setWindowTitle(son_titre)
        arrangement = QGridLayout()
        arrangement.addWidget(son_label)
        arrangement.addWidget(son_bouton)
        self.setLayout(arrangement)

def constuire_fenetre(): 
    mon_label = QLabel("Bienvenue dans l'IHM d'épidém.io")
    mon_bouton = QPushButton("Appuie sur moi !")

    ihm = Fenetre(
        "épidém.io",
        800,
        600,
        mon_label,
        mon_bouton
        )

    return ihm

if __name__ == "__main__":
    application = QApplication()

    ihm = constuire_fenetre()

    ihm.show()
    
    # Déboggage, rajoute une bordure à chaque élément de l'interface
    application.setStyleSheet("QWidget { border: 1px solid gray; }")
    sys.exit(application.exec())