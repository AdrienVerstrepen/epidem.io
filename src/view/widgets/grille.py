from PySide6.QtWidgets import *
from PySide6.QtCore import *
from classes import *
from pyqtgraph import *
import time
import numpy as np

class Grille_visualisation(QWidget):
    def __init__(self, 
                 taille_fenetre : dict,
                 nb_personnes : int = 10, 
                 nb_iterations : int = 20, 
                 taux_letalite : int = 5,
                 distance_infection : int = 50, 
                 taux_transmission : int = 30, 
                 temps_guerison : int = 20, 
                 taux_infectes : int = 4,
                 taux_immunodeprimes : int = 10
    ):
        super().__init__()
        self.sa_disposition = QGridLayout()
        self.setLayout(self.sa_disposition)

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
        self.visualisation = PlotWidget()
        self.sa_disposition.addWidget(self.visualisation)
        self.visualisation.setBackground('w')
        self.visualisation.showGrid(x=True, y=True, alpha=0.3) 
        # self.visualisation.hideAxis('bottom')
        # self.visualisation.hideAxis('left')

    def demarrer_simulation(self) :
        donnees = recuperer_points_personnes(self.sa_simulation.grille.carreaux)
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")

        personnes = donnees[2]
        
        self.nuage_de_points = ScatterPlotItem(size=10, spots=personnes)
        
        self.nuage_de_points.sigClicked.connect(afficher_information_personne)

        self.visualisation.addItem(self.nuage_de_points)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.actualiser_simulation)
        self.timer.start()

    def actualiser_simulation(self) -> None :
        self.sa_simulation.mise_a_jour_iteration()
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")
        self.nuage_de_points.setData(spots=recuperer_points_personnes(self.sa_simulation.grille.carreaux)[2])
        if (self.sa_simulation.iterations >= 100):
            self.timer.stop()
            print(self.sa_simulation.df_historique)

def recuperer_points_personnes(cases: list) -> tuple :
    ordonnees = []
    abscisses = []
    coordonnes_personnes = []
    for ordonnee, ligne in enumerate(cases):
        for abscisse, personne in enumerate(ligne):
            if personne:
                coordonnes_personnes.append({
                    'pos' : (abscisse, ordonnee),
                    'data' : personne,
                    'brush' : couleurs_personnes.get(personne[0].couleur),
                    'symbol' : "o",
                })
                ordonnees.append(ordonnee)
                abscisses.append(abscisse)
    return (abscisses, ordonnees, coordonnes_personnes)

def afficher_information_personne(graphique : ScatterPlotItem, points : list) -> None :
    for point in points:
        personne = point.data()
        print(str(personne[0]))

couleurs_personnes = {
    "rouge": "red",
    "vert": "green",
    "orange": "orange",
    "bleu": "blue"
}