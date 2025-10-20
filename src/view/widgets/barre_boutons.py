from PySide6.QtWidgets import *
from PySide6.QtCore import *
from view.widgets.boutons.demarrer import Bouton_demarrer
from view.widgets.boutons.pauser import Bouton_mettre_en_pause

class Barre_boutons(QWidget):
    def __init__(self, sa_fenetre):
        super().__init__()
        disposition = QGridLayout()
        self.sa_fenetre = sa_fenetre
        self.setLayout(disposition)

        self.boutons = []
        # bouton_lancer = QPushButton("Lancer la simulation")
        demarrer = Bouton_demarrer(self, "Démarrer la simulation")
        self.boutons.append(demarrer)

        bouton_mettre_en_pause = Bouton_mettre_en_pause(self, "Mettre en pause")
        self.boutons.append(bouton_mettre_en_pause)

        bouton_arreter = QPushButton("Arrêter")
        self.boutons.append(bouton_arreter)

        bouton_reinitialiser = QPushButton("Réinitialiser la simulation")
        self.boutons.append(bouton_reinitialiser)

        for i, bouton in enumerate(self.boutons):
            disposition.addWidget(bouton, 0, i)