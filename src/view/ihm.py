import sys
import random
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from fenetre import Fenetre

if __name__ == "__main__":
    application = QApplication()

    ihm = Fenetre()

    ihm.show()
    
    # Déboggage, rajoute une bordure à chaque élément de l'interface
    # application.setStyleSheet("QWidget { border: 1px solid gray; }")

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