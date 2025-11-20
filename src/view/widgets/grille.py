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
    """
    Composant contenant la représentation graphique de la simulation.

    Cette classe hérite de QWidget et s'occupe de lier le modèle (la simulation) 
    à l'IHM par le biais de différentes classes. Elle instancie et initialise la simulation 
    ainsi que le composant graphique portant la représentation.

    Attributs: 
        sa_fenetre (Fenetre): la fenetre, objet parent.
        sa_disposition (QGridLayout): objet hébergeant la visualisation des données
        taille_fenetre (dict): dictionnaire portant la hauteur et la largeur
        nb_personnes (int): le nombre de personnes de la simulation
        nb_iterations (int): le nombre d'iteration à l'instant T
        taux_letalite (int): le taux de mortalité de la maladie
        distance_infection (int): la distance à partir de laquelle une personne peut être infectée par une autre
        taux_transmission (int): le taux pour que l'infection se produise
        temps_guerison (int): le temps pour qu'une personne infectée devienne saine
        taux_infectes (int): le taux de personnes qui sont infectés au départ
        taux_immunodeprimes (int): le taux de personnes immunodeprimés au départ
        visualisation (PlotWidget): objet portant le nuage de point représentant les données
        sa_maladie (Maladie): maladie de la simulation
        sa_simulation (Simulation): la simulation instanciée
        nuage_de_points (ScatterPlotItem): le nuage de point qui visualise l'état T de la simulation
        en_cours (Boolean): indique si la simulation est en cours
        timer (QTimer): horloge permettant d'actualiser la simulation toutes les X millisecondes

    Méthodes:
        __init__ (Grille_visualisation): constructeur de la grille, instancie la disposition du composant 
                                         et des sous-composants.
        
        initialiser_simulation (None): fonction auxiliaire pour instancier les objets Maladie, Simulation 
                                       et initialiser la simulation
        
        creer_nuage_de_point (ScatterPlotItem): fonction auxiliaire qui instancie le nuage de point portant 
                                                les données de la simulation
        
        initialiser_nuage_de_point (None): fonction auxiliaire qui initialise le nuage de point en récupérant
                                       les données depuis la simulation et en ajout l'objet à la visualisation
        
        demarrer_simulation (None): fonction auxilaire qui démarre le déroulement de la simulation en 
                                    récupérant les paramètres saisis par l'utilisateur.
                                    Ici, elle met à jour la visualisation toutes les 250 millisecondes.
        
        mettre_en_pause_simulation (None): fonction auxiliaire pour mettre en pause ou reprendre la simulation.
        
        actualiser_simulation (None): fonction auxiliaire pour passer à l'itération d'après
        
        reinitialiser_simulation (None): arrête la simulation, récupère les paramètres saisis par l'utilisateur 
                                         et réinitialise une simulation avec ces nouvelles données.
        
        arreter_simulation (None): arrête l'actualisation la simulation à chaque X milliseconde.
        
        est_en_cours (Boolean): retourne l'état de la simulation
        
        recuperer_parametres_utilisateur (None): récupère les valeurs saisies par l'utilisateur 
                                                 dans les différents champs
    """
    def __init__(self, fenetre: "Fenetre", taille_fenetre : dict):

        super().__init__()

        self.sa_fenetre = fenetre

        self.sa_disposition = QGridLayout()
        self.setLayout(self.sa_disposition)

        self.taille_fenetre = taille_fenetre

        # Initialisation des paramètres de la simulation
        
        self.nb_personnes = 10
        self.nb_iterations = 20
        self.taux_letalite = 5
        self.distance_infection = 50
        self.taux_transmission = 30
        self.temps_guerison = 20
        self.taux_infectes = 4
        self.taux_immunodeprimes = 10

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
            immunite_apres_guerison=False,
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

        self.recuperer_parametres_utilisateur()

        self.initialiser_simulation()
        
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")
        
        self.initialiser_nuage_de_point()

        # gerer_la_taille_de_la_visualisation(self.visualisation)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.actualiser_simulation)
        self.timer.start()
        self.en_cours = True

    def mettre_en_pause_simulation(self, etat):
        if (etat) :
            self.timer.stop()
        else :
            self.timer.start()

    def actualiser_simulation(self) -> None :
        if not self.est_en_cours():
            return
        self.sa_simulation.mise_a_jour_iteration()
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")
        self.nuage_de_points.setData(spots=recuperer_points_personnes(self.sa_simulation.grille.carreaux)[2])
        if (self.sa_simulation.iterations >= 100):
            self.arreter_simulation()
            print(self.sa_simulation.df_historique)

        print("DEBUG PERSONNES")
        for personne in self.sa_simulation.liste_personnes:
            print(personne)

    def reinitialiser_simulation(self):
        self.arreter_simulation()
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
        self.temps_guerison = self.sa_fenetre.ses_parametres.champ_temps_guerison.recuperer_valeur_depuis_champ()
        self.taux_infectes = self.sa_fenetre.ses_parametres.slider_infectes.value()
        self.taux_letalite = self.sa_fenetre.ses_parametres.slider_letalite.value()
        self.taux_transmission = self.sa_fenetre.ses_parametres.slider_transmission.value()
        self.taux_immunodeprimes = self.sa_fenetre.ses_parametres.slider_immunodeprime.value()

# def gerer_la_taille_de_la_visualisation(widget_graphique: PlotWidget):
#     visualisation = widget_graphique.getViewBox()
#     visualisation.disableAutoRange()
#     visualisation.setLimits(xMin=-15, xMax=15, yMin=-5, yMax=10)
#     visualisation.setRange(xRange=(-15, 15), yRange=(5, 10))

#     x = widget_graphique.getAxis('bottom')
#     y = widget_graphique.getAxis('left')

#     x.setTickSpacing(major=1, minor=0.5)
#     y.setTickSpacing(major=1, minor=0.5)

def recuperer_points_personnes(cases: list) -> tuple :
    """
    Récupère la position des personnes

    Paramètres:
        cases (List): les cases contenant les personnes présentes dans la simulation

    Retourne:
       tuple: comportant un tableau des abscisses, des ordonnées et un tableau de coordonnée avec la personne associée.
    """
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

def afficher_information_personne(points : list) -> None :
    """
    Permet de récupérer les informations d'une personne cliquée

    Parametres: 
        points (List): la liste des points du graphique

    Retourne: 
        None
    """
    for point in points:
        personne = point.data()
        print(str(personne[0]))

couleurs_personnes = {
    "rouge": "red",
    "vert": "green",
    "orange": "orange",
    "bleu": "blue"
}