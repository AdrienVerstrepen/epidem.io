from PySide6.QtWidgets import *
from PySide6.QtCore import *
from classes import *

class Grille_visualisation(QWidget):
    def __init__(self, taille_fenetre):
        super().__init__()
        disposition = QGridLayout()
        self.setLayout(disposition)

        self.taille_fenetre = taille_fenetre

        self.sa_maladie = Maladie(
            taux_letalite=5,
            distance_infection=10,
            risque_transmission=30,
            immunite_apres_guerison=True,
            temps_guerison=10
        )

        self.sa_simulation = Simulation(
            self.sa_maladie, 
            largeur_fenetre=self.taille_fenetre[0], 
            hauteur_fenetre=self.taille_fenetre[1], 
            nb_personnes=50
        )

        self.sa_simulation.initialiser_population(
            largeur_fenetre=self.taille_fenetre[0], 
            hauteur_fenetre=self.taille_fenetre[1],
            pourcentage_infectes=2,
            pourcentage_immunodeprimes=10
        )

        for ligne in range(int(self.sa_simulation.nb_personnes/2)):
            for colonne in range(int(self.sa_simulation.nb_personnes/2)):
                case = QPushButton(f"{ligne}, {colonne}")
                disposition.addWidget(case, ligne, colonne)