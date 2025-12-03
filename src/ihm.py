import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from .view.fenetre import Fenetre

if __name__ == "__main__":
    application = QApplication()
    largeur = 800
    hauteur = 600
    taille_fenetre = {"largeur": largeur,"hauteur": hauteur}
    ihm = Fenetre(taille_fenetre)
    ihm.show()
    # Déboggage, rajoute une bordure à chaque élément de l'interface
    # application.setStyleSheet("QWidget { border: 1p x solid gray; }")
    sys.exit(application.exec())