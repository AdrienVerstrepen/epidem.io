from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ...algorithmie.maladie import *
from ...algorithmie.grille import *
from ...algorithmie.personne import *
from ...algorithmie.simulation import *
from pyqtgraph import *

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fenetre import Fenetre

class Grille_visualisation(QWidget):
    """
    Composant contenant la représentation graphique de la simulation.

    Cette classe hérite de QWidget et s'occupe de lier le modèle (la simulation) 
    à l'IHM par le biais de différentes classes. Elle instancie et initialise la simulation 
    ainsi que le composant graphique portant la représentation.
    """
    sa_fenetre : "Fenetre"
    """La fenêtre, objet parent."""
    
    sa_disposition : "QGridLayout"
    """Objet hébergeant la visualisation des données."""
    
    taille_fenetre : "dict"
    """Dictionnaire contenant la hauteur et la largeur de la fenêtre."""
    
    nb_personnes : "int"
    """Nombre de personnes de la simulation."""
    
    nb_iterations : "int"
    """Nombre d'itérations à l'instant T."""
    
    taux_letalite : "int"
    """Taux de mortalité de la maladie."""
    
    distance_infection : "int"
    """Distance à partir de laquelle une personne peut être infectée par une autre."""
    
    taux_transmission : "int"
    """Taux de transmission de l'infection."""
    
    temps_guerison : "int"
    """Temps pour qu'une personne infectée devienne saine."""
    
    taux_infectes : "int"
    """Taux de personnes infectées au départ."""
    
    taux_immunodeprimes : "int"
    """Taux de personnes immunodéprimées au départ."""
    
    visualisation : "PlotWidget"
    """Objet portant le nuage de points représentant les données."""
    
    sa_maladie : "Maladie"
    """Maladie de la simulation."""
    
    sa_simulation : "Simulation"
    """Simulation instanciée."""
    
    nuage_de_points : "ScatterPlotItem"
    """Nuage de points visualisant l'état T de la simulation."""
    
    en_cours : "bool"
    """Indique si la simulation est en cours."""
    
    timer : "QTimer"
    """Horloge permettant d'actualiser la simulation toutes les X millisecondes."""
    
    def __init__(self, fenetre: "Fenetre", taille_fenetre : dict) -> "Grille_visualisation":
        """
        Constructeur de la grille, instancie la disposition du composant et des sous-composants.
        
        :param fenetre: La fenêtre parente
        :type fenetre: "Fenetre"
        :param taille_fenetre: La taille de cette fenêtre parente
        :type taille_fenetre: dict
        """
        super().__init__()
        self.sa_fenetre = fenetre
        self.sa_disposition = QGridLayout()
        self.setLayout(self.sa_disposition)
        self.taille_fenetre = taille_fenetre
        self.sa_simulation = None
        self.distance_infection = None
        dimension_graphique = 520
        self.rendre_visible_distance_contagion = False
        # Récupération des données initialisées
        self.visualisation = PlotWidget()
        self.sa_disposition.addWidget(self.visualisation)
        self.visualisation.setBackground('w')
        self.visualisation.getViewBox().disableAutoRange()
        self.visualisation.getViewBox().setAutoPan(False)
        self.visualisation.getViewBox().setLimits(
            xMin=-10, xMax=dimension_graphique,
            yMin=-10, yMax=dimension_graphique,
            minXRange=dimension_graphique, maxXRange=dimension_graphique,
            minYRange=dimension_graphique, maxYRange=dimension_graphique
        )
        self.visualisation.setMenuEnabled(False)
        self.visualisation.hideButtons()
        self.visualisation.getViewBox().setMouseEnabled(x=False, y=False)
        self.visualisation.hideAxis('bottom')
        self.visualisation.hideAxis('left')

    def initialiser_simulation(self) -> None:
        """
        Fonction auxiliaire pour instancier les objets Maladie, Simulation et initialiser la simulation.
        """
        self.sa_maladie = Maladie(
            taux_letalite=self.taux_letalite,
            distance_infection=self.distance_infection,
            risque_transmission=self.taux_transmission,
            immunite_apres_guerison=self.immunite,
            temps_guerison=self.temps_guerison
        )

        self.sa_simulation = Simulation(
            self.sa_maladie, 
            largeur_fenetre=500, 
            hauteur_fenetre=500, 
            nb_personnes=self.nb_personnes,
            taux_naissance=self.taux_natalite/100
        )

        self.sa_simulation.initialiser_population(
            largeur_fenetre=500, 
            hauteur_fenetre=500,
            pourcentage_infectes=self.taux_infectes,
            pourcentage_immunodeprimes=self.taux_immunodeprimes
        )

    def creer_nuage_de_point(self, taille_point : int, personnes : list) -> ScatterPlotItem:
        """
        Fonction auxiliaire qui instancie le nuage de points portant les données de la simulation.
        
        :param taille_point: La taille à choisir pour le point
        :param personnes: Le tableau des personnes
        :return: Le graphique ScatterPlotItem porteur des points représentant les personnes.
        """
        if not taille_point:
            taille_point = 10
        graphique = ScatterPlotItem(size=taille_point, spots=personnes)
        return graphique

    def initialiser_nuage_de_point(self) -> None:
        """
        Fonction auxiliaire qui instancie le nuage de points 
        avec les données de la première itération
        """
        personnes = self.recuperer_points_personnes(self.sa_simulation.liste_personnes)
        nb_reel_personnes = (len(self.sa_simulation.liste_personnes))
        
        if nb_reel_personnes >= 200 and nb_reel_personnes <= 300:
            taille_point = 6
        if nb_reel_personnes > 300 and nb_reel_personnes <= 400:
            taille_point = 2
        else:
            taille_point = 10
        self.nuage_de_points = self.creer_nuage_de_point(taille_point, personnes)

        self.nuage_de_points.sigClicked.connect(afficher_information_personne)
        
        self.visualisation.addItem(self.nuage_de_points)

    def demarrer_simulation(self) -> None :
        """
        Fonction auxiliaire qui démarre la simulation en récupérant les paramètres saisis 
        par l'utilisateur. Met à jour la visualisation toutes les 250 millisecondes.
        """
        self.recuperer_parametres_utilisateur()

        self.initialiser_simulation()
        
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")
        
        self.initialiser_nuage_de_point()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.actualiser_simulation)
        self.timer.start()
        self.en_cours = True

    def mettre_en_pause_simulation(self, etat : bool) -> None:
        """
        Méthode permettant de mettre en pause l'horloge
        en fonction de l'état passé en paramètre
        
        :param etat: Le booléen indiquant l'état de la simulation
        """
        if (etat) :
            self.timer.stop()
        else :
            self.timer.start()

    def actualiser_simulation(self) -> None:
        """
        Fonction auxiliaire pour passer à l'itération suivante.
        """
        # i = 0
        # for vivant in [p for p in self.sa_simulation.liste_personnes if p.etat != "mort"] :
        #     i += 1
        # print(f"Nombre de vivants : {i}")
        if not self.est_en_cours():
            return
        self.sa_simulation.mise_a_jour_iteration()
        self.visualisation.setTitle(f"Itération n°{self.sa_simulation.iterations}")
        if self.isActiveWindow():
            self.nuage_de_points.setData(spots=self.recuperer_points_personnes(self.sa_simulation.liste_personnes))

    def reinitialiser_simulation(self) -> None:
        """
        Arrête la simulation, récupère les paramètres saisis par l'utilisateur et réinitialise la simulation avec ces nouvelles données.
        """
        self.arreter_simulation()
        self.visualisation.setTitle(f"")
        self.recuperer_parametres_utilisateur()
        self.initialiser_simulation()
        self.nuage_de_points.setData([])

    def arreter_simulation(self):
        """
        Arrête l'actualisation de la simulation.
        """
        self.timer.stop()
        self.en_cours = False
        
    def est_en_cours(self) -> bool:
        """
        Retourne l'état de la simulation.
        """
        return self.en_cours

    def recuperer_parametres_utilisateur(self):
        """
        Récupère les valeurs saisies par l'utilisateur dans les différents champs.
        """
        self.nb_personnes = self.sa_fenetre.ses_parametres.champ_nb_personnes.value()
        self.temps_guerison = self.sa_fenetre.ses_parametres.champ_temps_guerison.recuperer_valeur_depuis_champ()
        self.taux_infectes = self.sa_fenetre.ses_parametres.champ_infectes.value()
        self.taux_letalite = self.sa_fenetre.ses_parametres.champ_letalite.value()
        self.taux_transmission = self.sa_fenetre.ses_parametres.champ_transmission.value()
        self.taux_immunodeprimes = self.sa_fenetre.ses_parametres.champ_immunodeprime.value()
        self.immunite = self.sa_fenetre.ses_parametres.champ_immunite.isChecked()
        self.taux_natalite = self.sa_fenetre.ses_parametres.champ_natalite.value()
        self.distance_infection = self.sa_fenetre.ses_parametres.champ_distance_infection.recuperer_valeur_depuis_champ()

    def recuperer_points_personnes(self, personnes: list[Personne]) -> list :
        """
        Récupère la position des personnes dans la simulation
        
        :param self: Description
        :param personnes: Description
        :type personnes: list[Personne]
        :return: La liste des personnes, avec leur position, leur couleur et leur symbole
        """
        afficher_morts = self.sa_fenetre.ses_parametres.champ_morts_visibles.isChecked()
        coordonnes_personnes = []
        for personne in personnes:
            if afficher_morts:
                coordonnes_personnes.append({
                    'pos' : personne.position,
                    'data' : personne,
                    'brush' : couleurs_personnes.get(personne.couleur),
                    'symbol' : 'star' if (personne.medecin == 1) else 'o',
                    'size' : 15 if (personne.medecin == 1) else 10
                })
            elif personne.cooldown_affichage_apres_mort != 0:
                coordonnes_personnes.append({
                    'pos' : personne.position,
                    'data' : personne,
                    'brush' : couleurs_personnes.get(personne.couleur),
                    'symbol' : 'star' if (personne.medecin == 1) else 'o',
                    'size' : 15 if (personne.medecin == 1) else 10
                })
        if self.rendre_visible_distance_contagion == True:
            self.rendre_visible_distance_contagion(coordonnes_personnes)
        return coordonnes_personnes

    def rendre_visible_distance_contagion(self, personnes) -> None:
        """
        Fonction auxiliaire qui affiche la distance de la 
        contagion de la maladie autour d'une personne
        :param personnes: La liste des personnes
        """
        x, y = personnes[0]['pos']
        diametre = self.distance_infection
        couleur = (255, 0, 0)

        spot_cercle = {
            'pos': (x, y),
            'size': diametre,
            'pen': mkPen(couleur, width=2),
            'brush': None,
            'symbol': 'o'
        }
        personnes.append(spot_cercle)

def afficher_information_personne(scatter, points : list) -> None :
    """
    Permet d'afficher les informations d'une personne cliquée
    
    :param scatter: Le graphique sur lequel l'écoute du signal est placée
    :param points: Les points du graphique
    :type points: list
    """
    for point in points:
        data = point.data()
        if type(data) == Personne:
            print(str(data))

couleurs_personnes = {
    "rouge": "red",
    "vert": "green",
    "orange": "orange",
    "bleu": "blue"
}
"""Dictionnaire de traduction des couleurs du format
utilisé dans la partie algorithmie"""