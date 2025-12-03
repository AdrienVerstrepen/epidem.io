from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING
from .boutons.demarrer import Bouton_demarrer
from .boutons.pauser import Bouton_mettre_en_pause
from .boutons.reinitialiser import Bouton_reinitialiser
from .boutons.arreter import Bouton_arreter

if TYPE_CHECKING:
    from ..fenetre import Fenetre

class Barre_boutons(QGroupBox):
    """
    Composant graphique contenant les différents boutons de l'interface.

    Cette classe hérite de QGroupBox et s'occupe d'instancier les différents boutons.

    Attributs:
        sa_disposition (QGridLayout): objet hébergeant les différents boutons
        sa_fenetre (Fenetre): la fenetre, objet parent
        boutons (List): ensemble des boutons à instancier
        bouton_demarrer (Bouton_demarrer): bouton permettant de lancer la simulation
        bouton_mettre_en_pause (Bouton_mettre_en_pause): bouton permettant de 
                                                         mettre en pause ou 
                                                         reprendre la simulation
        bouton_arreter (Bouton_arreter): bouton permettant d'arrêter définitivement 
                                         la simulation en cours
        bouton_reinitialiser (Bouton_reinitialiser): bouton permettant de réinitialiser 
                                                     les états des boutons et de la 
                                                     simulation

    Méthodes:
        get_bouton_demarrer (Bouton_demarrer): getter du bouton de démarrage
        get_bouton_pause (Bouton_mettre_en_pause): getter du bouton de mise en pause
        get_bouton_reinitialiser (Bouton_reinitialiser): getter du bouton de réinitialisation
    """
    def __init__(self, sa_fenetre: "Fenetre"):
        super().__init__()
        self.sa_disposition = QGridLayout()
        self.sa_fenetre = sa_fenetre
        self.setLayout(self.sa_disposition)

        self.boutons = []
        self.bouton_demarrer = Bouton_demarrer(self, "Démarrer la simulation")
        self.boutons.append(self.bouton_demarrer)

        self.bouton_mettre_en_pause = Bouton_mettre_en_pause(self, "Mettre en pause")
        self.boutons.append(self.bouton_mettre_en_pause)

        self.bouton_arreter = Bouton_arreter(self, "Arrêter")
        self.boutons.append(self.bouton_arreter)

        self.bouton_reinitialiser = Bouton_reinitialiser(self, "Réinitialiser la simulation")
        self.boutons.append(self.bouton_reinitialiser)

        for i, bouton in enumerate(self.boutons):
            self.sa_disposition.addWidget(bouton, 0, i)

    def get_bouton_demarrer(self) -> "Bouton_demarrer": 
        return self.bouton_demarrer
    
    def get_bouton_pause(self) -> "Bouton_mettre_en_pause":
        return self.bouton_mettre_en_pause
    
    def get_bouton_reinitialiser(self) -> "Bouton_reinitialiser":
        return self.bouton_reinitialiser