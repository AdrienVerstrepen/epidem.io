from PySide6.QtWidgets import *
from PySide6.QtCore import *
from classes import *
from pyqtgraph import *
import time
import numpy as np

class Grille_visualisation(QWidget):
    def __init__(self, 
                 taille_fenetre, 
                 nb_personnes=10, 
                 nb_iterations=20, 
                 taux_letalite=5, 
                 distance_infection=2, 
                 taux_transmission=30, 
                 temps_guerison=10, 
                 taux_infectes=2, 
                 taux_immunodeprimes=10
    ):
        super().__init__()
        disposition = QGridLayout()
        self.setLayout(disposition)

        self.taille_fenetre = taille_fenetre

        # Initialisation des paramètres de la simulation
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

        # Récupération des données initialisées
        donnees = recuperer_points_personnes(self.sa_simulation.grille.carreaux)
        
        visualisation = PlotWidget()
        visualisation.setBackground('w')
        visualisation.showGrid(x=True, y=True, alpha=0.3) 

        personnes = donnees[2]
        
        nuage_de_points = ScatterPlotItem(size=10, spots=personnes)
        
        nuage_de_points.sigClicked.connect(personne_selectionnee)

        visualisation.addItem(nuage_de_points)

        disposition.addWidget(visualisation)

def recuperer_points_personnes(cases):
    ordonnees = []
    abscisses = []
    coordonnes_personnes = []
    for ordonnee, ligne in enumerate(cases):
        for abscisse, personne in enumerate(ligne):
            if personne:
                coordonnes_personnes.append({
                    'pos' : (abscisse, ordonnee),
                    'data' : personne,
                    'symbol' : "o",

                })
                ordonnees.append(ordonnee)
                abscisses.append(abscisse)
    return (abscisses, ordonnees, coordonnes_personnes)

def personne_selectionnee(plot, points):
    for pt in points:
        objet = pt.data()
        print("Objet lié :", str(objet[0]))