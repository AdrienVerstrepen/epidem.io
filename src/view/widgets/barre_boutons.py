from PySide6.QtWidgets import *
from PySide6.QtCore import *
from .boutons.demarrer import Bouton_demarrer
from .boutons.pauser import Bouton_mettre_en_pause
from .boutons.reinitialiser import Bouton_reinitialiser

class Barre_boutons(QWidget):
    def __init__(self, sa_fenetre):
        super().__init__()
        self.sa_disposition = QGridLayout()
        self.sa_fenetre = sa_fenetre
        self.setLayout(self.sa_disposition)

        self.boutons = []
        # bouton_lancer = QPushButton("Lancer la simulation")
        self.bouton_demarrer = Bouton_demarrer(self, "Démarrer la simulation")
        self.boutons.append(self.bouton_demarrer)

        self.bouton_mettre_en_pause = Bouton_mettre_en_pause(self, "Mettre en pause")
        self.boutons.append(self.bouton_mettre_en_pause)

        bouton_arreter = QPushButton("Arrêter")
        self.boutons.append(bouton_arreter)

        self.bouton_reinitialiser = Bouton_reinitialiser(self, "Réinitialiser la simulation")
        self.boutons.append(self.bouton_reinitialiser)

        for i, bouton in enumerate(self.boutons):
            self.sa_disposition.addWidget(bouton, 0, i)

    def get_bouton_demarrer(self) -> Bouton_demarrer: 
        return self.bouton_demarrer
    
    def get_bouton_pause(self) -> Bouton_mettre_en_pause:
        return self.bouton_mettre_en_pause
    
    def get_bouton_reinitialiser(self) -> Bouton_reinitialiser:
        return self.bouton_reinitialiser