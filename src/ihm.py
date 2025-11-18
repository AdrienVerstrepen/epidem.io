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

# Exemple doc string fonction : 
"""
Ce que la fonction fait

Parametres:
    a (int): First number.
    b (int): Second number.

Retourne:
    int: Product of a and b.
"""

# Exemple doc string classe
"""
Ce que la classe est

Parametres: (s'il y'en a)
    a (int): First number.
    b (int): Second number.

Attributs: 
    nom (type): ce qu'il est

Méthodes:
    nom (type de retour): ce qu'elle fait

"""