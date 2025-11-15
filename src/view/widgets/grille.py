from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ...classes import *
from pyqtgraph import *
import time
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fenetre import Fenetre

class Grille_visualisation(QWidget):
    def __init__(self, 
                taille_fenetre : dict,
                nb_personnes : int, 
                #  nb_iterations : int = 20, 
                #  taux_letalite : int = 5,
                #  distance_infection : int = 50, 
                #  taux_transmission : int = 30, 
                #  temps_guerison : int = 20, 
                #  taux_infectes : int = 4,
                #  taux_immunodeprimes : int = 10,
                fenetre: Fenetre
                ):
        
        super().__init__()

        self.sa_fenetre = fenetre

        self.sa_disposition = QGridLayout()
        self.setLayout(self.sa_disposition)

        self.taille_fenetre = taille_fenetre

        # self.taux_infectes = taux_infectes
        # self.taux_immunodeprimes = taux_immunodeprimes

        # Initialisation des paramètres de la simulation
        
        self.nb_personnes = 10
        self.nb_iterations = 20
        self.taux_letalite = 5
        self.distance_infection = 50
        self.taux_transmission = 30
        self.temps_guerison = 20
        self.taux_infectes = 4
        self.taux_immunodeprimes = 10

        self.recuperer_parametres_utilisateur()

        self.initialiser_simulation()

        # Récupération des données initialisées
        self.visualisation = PlotWidget()
        self.sa_disposition.addWidget(self.visualisation)
        self.visualisation.setBackground('w')
        self.visualisation.showGrid(x=True, y=True, alpha=0.3) 
        self.visualisation.hideAxis('bottom')
        self.visualisation.hideAxis('left')

    def initialiser_simulation(self):
        self.sa_maladie = Maladie(
            taux_letalite=self.taux_letalite,
            distance_infection=self.distance_infection,
            risque_transmission=self.taux_transmission,
            immunite_apres_guerison=True,
            temps_guerison=self.temps_guerison
        )

        self.sa_simulation = Simulation(
            self.sa_maladie, 
            largeur_fenetre=self.taille_fenetre["largeur"], 
            hauteur_fenetre=self.taille_fenetre["hauteur"], 
            nb_personnes=self.nb_personnes
        )

        self.sa_simulation.initialiser_population(
            largeur_fenetre=self.taille_fenetre["largeur"], 
            hauteur_fenetre=self.taille_fenetre["hauteur"],
            pourcentage_infectes=self.taux_infectes,
            pourcentage_immunodeprimes=self.taux_immunodeprimes
        )

    def creer_nuage_de_point(self, taille_point, personnes):
        if not taille_point:
            taille_point = 10
        graphique = ScatterPlotItem(size=taille_point, spots=personnes)
        
        return graphique

    def initialiser_nuage_de_point(self):
        donnees = recuperer_points_personnes(self.sa_simulation.grille.carreaux)
        personnes = donnees[2]
        taille_point = 10
        self.nuage_de_points = self.creer_nuage_de_point(taille_point, personnes)

        self.nuage_de_points.sigClicked.connect(afficher_information_personne)
        
        self.visualisation.addItem(self.nuage_de_points)

    def demarrer_simulation(self) :
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")
        
        self.initialiser_nuage_de_point()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.actualiser_simulation)
        self.timer.start()
        self.en_cours = True

    def mettre_en_pause_simulation(self, etat):
        if (etat) :
            self.timer.stop()
        else :
            self.timer.start()

    def actualiser_simulation(self) -> None :
        if not self.en_cours:
            return
        self.sa_simulation.mise_a_jour_iteration()
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")
        self.nuage_de_points.setData(spots=recuperer_points_personnes(self.sa_simulation.grille.carreaux)[2])
        if (self.sa_simulation.iterations >= 20):
            self.timer.stop()
            print(self.sa_simulation.df_historique)

    def reinitialiser_simulation(self):
        self.mettre_en_pause_simulation(True)
        self.visualisation.setTitle(f"")
        self.recuperer_parametres_utilisateur()
        self.initialiser_simulation()
        self.nuage_de_points.setData([])

    def arreter_simulation(self):
        self.timer.stop()
        self.en_cours = False
        
    def est_en_cours(self):
        return self.en_cours

    def recuperer_parametres_utilisateur(self):
        self.nb_personnes = self.sa_fenetre.ses_parametres.champ_nb_personnes.value()
        # self.nb_iterations = nb_iterations
        # self.taux_letalite = taux_letalite
        # self.distance_infection = distance_infection
        # self.taux_transmission = taux_transmission
        # self.temps_guerison = temps_guerison
        # self.taux_infectes = taux_infectes
        # self.taux_immunodeprimes = taux_immunodeprimes

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