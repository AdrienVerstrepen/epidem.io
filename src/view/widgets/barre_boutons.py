from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Barre_boutons(QWidget):
    def __init__(self):
        super().__init__()
        disposition = QHBoxLayout()
        self.setLayout(disposition)

        self.boutons = []
        bouton_lancer = QPushButton("Lancer la simulation")
        self.boutons.append(bouton_lancer)
        bouton_mettre_en_pause = QPushButton("Mettre en pause")
        self.boutons.append(bouton_mettre_en_pause)
        bouton_arreter = QPushButton("Arrêter")
        self.boutons.append(bouton_arreter)
        bouton_reinitialiser = QPushButton("Réinitialiser la simulation")
        self.boutons.append(bouton_reinitialiser)

        for bouton in self.boutons:
            disposition.addWidget(bouton)

        disposition.addStretch()