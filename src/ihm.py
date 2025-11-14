import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from .view.fenetre import Fenetre

if __name__ == "__main__":
    application = QApplication()
    largeur = 800
    hauteur = 600
    taille_fenetre = {"largeur": largeur,"hauteur": hauteur}
    nb_personnes = 100
    ihm = Fenetre(nb_personnes, taille_fenetre)
    ihm.show()
    # Déboggage, rajoute une bordure à chaque élément de l'interface
    # application.setStyleSheet("QWidget { border: 1p x solid gray; }")
    sys.exit(application.exec())

# Exemple doc string : 
"""
Ce que la fonction fait

Args:
    a (int): First number.
    b (int): Second number.

Returns:
    int: Product of a and b.
"""