from PySide6.QtWidgets import *
from PySide6.QtCore import *
from classes import *
from pyqtgraph import *

class Grille_visualisation(QWidget):
    def __init__(self, 
                 taille_fenetre, 
                 nb_personnes=10, 
                 nb_iterations=20, 
                 taux_letalite=5, 
                 distance_infection=10, 
                 taux_transmission=30, 
                 temps_guerison=10, 
                 taux_infectes=2, 
                 taux_immunodeprimes=10
    ):
        super().__init__()
        disposition = QGridLayout()
        self.setLayout(disposition)

        self.taille_fenetre = taille_fenetre

        self.sa_maladie = Maladie(
            taux_letalite=taux_letalite,
            distance_infection=distance_infection,
            risque_transmission=taux_transmission,
            immunite_apres_guerison=True,
            temps_guerison=temps_guerison
        )

        self.sa_simulation = Simulation(
            self.sa_maladie, 
            largeur_fenetre=self.taille_fenetre["largeur"], 
            hauteur_fenetre=self.taille_fenetre["hauteur"], 
            nb_personnes=nb_personnes
        )

        self.sa_simulation.initialiser_population(
            largeur_fenetre=self.taille_fenetre["largeur"], 
            hauteur_fenetre=self.taille_fenetre["hauteur"],
            pourcentage_infectes=taux_infectes,
            pourcentage_immunodeprimes=taux_immunodeprimes
        )

        # visualisation = ScatterPlotWidget()
        # disposition.addWidget(visualisation)

        # nb_iterations = 20
        # for i in range(nb_iterations):
        #     debut_temps = time.time()
        #     self.sa_simulation.mise_a_jour_iteration()
        #     fin_temps = time.time()
        #     print(f"{i} :", fin_temps-debut_temps)