from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Grille(QWidget):
    def __init__(self):
        super().__init__()
        disposition = QGridLayout()
        self.setLayout(disposition)

        # Exemple avec une grille 3x3
        for ligne in range(3):
            for colonne in range(3):
                btn = QPushButton(f"{ligne},{colonne}")
                disposition.addWidget(btn, ligne, colonne)
