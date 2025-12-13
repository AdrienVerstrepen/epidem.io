from PySide6.QtWidgets import *
from PySide6.QtCore import *
from .sliders.taux_letalite import Slider_letalite
from .sliders.taux_transmission import Slider_transmission
from .sliders.taux_immunodeprimes import Slider_immunodeprime
from .sliders.taux_infectes import Slider_infectes
from .champs.nombre_personnes import Champ_nb_personnes
from .champs.temps_guerison import Champ_temps_guerison
from .champs.immunite import Champ_immunite

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fenetre import Fenetre

class Parametres(QGroupBox):
	"""
	Composant graphique portant les champs de saisi des paramètres
	modifiables par l'utilisateur

	Hérite de QGroupBox et instancie les champs et leurs labels associés

	Attributs: 
		sa_fenetre (Fenetre): son objet parent Fenetre
		sa_disposition (QVBoxLayout): le layout suivi par ses composants
		label_letalite (QLabel): Le QLabel associé au slider letalite
		slider_letalite (Slider_letalite): Le composant à glisser permettant de récupérer la valeur pour le taux de létalité
		label_infectes (QLabel): Le QLabel associé au slider infectés
		slider_infectes (Slider_infectes): Composant permettant de récupérer la valeur du taux de personnes infectés
		label_transmission (QLabel): Le QLabel associé au slider transmissio
		slider_transmission (Slider_transmission): Composant récupérant la valeur du taux de transmission de la maladie
		label_immunodeprime (QLabel): QLabel associé au slider immunodéprimé
		slider_immunodeprime (Slider_immunodeprime): Composant récupérant la valeur du taux de personne immunodéprimés de la maladie
		label_nb_personnes (QLabel): QLabel associé au champ du nombre de personnes
		champ_nb_personnes (Champ_nb_personnes): Composant récupérant la valeur du nombre de personnes
		label_temps_guerison (QLabel): QLabel associé au champ du temps de guérison
		champ_temps_guerison (Champ_temps_guerison): Composant récupérant la valeur du temps de guérison de la maladie
		label_immunite (QLabel): QLabel associé au champ activant ou non l'immunité après guérison
		champ_immunite (Champ_immunite): Composant récupérant la possibilté ou non d'avoir une immunité

	Méthodes:
		initialiser_parametres (None): fonction auxiliaire qui initialie tous les composants
		initialiser_slider_letalite (None): 
		initialiser_slider_infectes (None): 
		initialiser_slider_transmission (None): 
		initialiser_slider_immunodeprime (None): 
		initialiser_champ_nb_personnes (None): 
		initialiser_champ_temps_guerison (None): 
		initialiser_champ_immunite (None): 

	"""
	def __init__(self, fenetre: "Fenetre"):
		super().__init__()

		self.sa_fenetre = fenetre
		self.sa_disposition = QVBoxLayout()
		self.setLayout(self.sa_disposition)

		self.initialiser_parametres()
		
		self.afficher_distance_infection = QCheckBox("Afficher la distance d'infection", self)
		self.afficher_distance_infection.stateChanged.connect(self.gerer_affichage_distance_contagion)

		self.sa_disposition.addWidget(self.afficher_distance_infection)
		
		self.sa_disposition.addStretch()

	def initialiser_parametres(self):
		self.initialiser_slider_letalite("Taux de létalité de la maladie", 5)

		self.initialiser_champ_nb_personnes("Effectif de la population", 200)

		self.initialiser_slider_transmission("Pourcentage de transmission", 20)
		
		self.initialiser_slider_immunodeprime("Pourcentage de personnes immunodéprimées", 15)

		self.initialiser_slider_infectes('Pourcentage de patient(s) "0"', 10)

		self.initialiser_champ_temps_guerison("Duree d'infection de la maladie", 20)

		self.initialiser_champ_immunite("Immunité après guérison", False)

	def initialiser_slider_letalite(self, nom: str, valeur_defaut: int):
		self.label_letalite = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_letalite)
		
		self.slider_letalite = Slider_letalite(self, nom)
		self.slider_letalite.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_letalite)
		self.label_letalite.setToolTip("Le pourcentage de mortalité d'une personne infectée à chaque itération")

		self.slider_letalite.valueChanged.connect(self.slider_letalite.changement_valeur)

	def initialiser_slider_infectes(self, nom: str, valeur_defaut: int):
		self.label_infectes = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_infectes)
		
		self.slider_infectes = Slider_infectes(self, nom)
		self.slider_infectes.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_infectes)

		self.slider_infectes.valueChanged.connect(self.slider_infectes.changement_valeur)
		self.label_infectes.setToolTip("Le pourcentage de personnes infectées au lancement d'une simulation")
	
	def initialiser_slider_transmission(self, nom: str, valeur_defaut: int):
		self.label_transmission = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_transmission)
		
		self.slider_transmission = Slider_transmission(self, nom)
		self.slider_transmission.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_transmission)

		self.slider_transmission.valueChanged.connect(self.slider_transmission.changement_valeur)
		self.label_transmission.setToolTip("Le pourcentage qu'une personne infectée transmette la maladie à une autre")

	def initialiser_slider_immunodeprime(self, nom: str, valeur_defaut: int):
		self.label_immunodeprime = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_immunodeprime)
		
		self.slider_immunodeprime = Slider_immunodeprime(self, nom)
		self.slider_immunodeprime.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_immunodeprime)

		self.slider_immunodeprime.valueChanged.connect(self.slider_immunodeprime.changement_valeur)
		self.label_immunodeprime.setToolTip("Le pourcentage de personnes immunodéprimées au lancement de la simulation")

	def initialiser_champ_nb_personnes(self, nom: str, valeur_defaut: int):	
		self.label_nb_personnes = QLabel(f"{nom} : {valeur_defaut}")
		self.sa_disposition.addWidget(self.label_nb_personnes)

		self.champ_nb_personnes = Champ_nb_personnes(self, nom)
		self.champ_nb_personnes.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.champ_nb_personnes)

		self.champ_nb_personnes.valueChanged.connect(self.champ_nb_personnes.changement_valeur)
		self.label_nb_personnes.setToolTip("Le nombre de personnes au lancement d'une simulation")

	def initialiser_champ_temps_guerison(self, nom: str, valeur_defaut: int):
		self.label_temps_guerison = QLabel(f"{nom} : ")
		self.sa_disposition.addWidget(self.label_temps_guerison)

		self.champ_temps_guerison = Champ_temps_guerison(self, nom)
		self.sa_disposition.addWidget(self.champ_temps_guerison)

		self.champ_temps_guerison.currentIndexChanged.connect(self.champ_temps_guerison.changement_valeur)
		self.label_temps_guerison.setToolTip("Le temps pour guérir de la maladie")

	def initialiser_champ_immunite(self, nom: str, valeur_defaut: int):
		self.label_immunite = QLabel(f"{nom} : {valeur_defaut}")
		self.sa_disposition.addWidget(self.label_immunite)

		self.champ_immunite = Champ_immunite(self, nom)
		self.sa_disposition.addWidget(self.champ_immunite)

		self.champ_immunite.stateChanged.connect(self.champ_immunite.changement_valeur)
		self.label_immunite.setToolTip("La possibilité ou non d'être immunisé après avoir guéri de la maladie")

	def initialiser_dropdown_distance_infection(self, nom: str, valeur_defaut: int):
		self.label_dist_infection = QLabel(f"{nom} : {valeur_defaut}")
		self.sa_disposition.addWidget(self.label_dist_infection)

		self.champ_dist_infection = Champ_distance_infection(self, nom)
		self.sa_disposition.addWidget(self.champ_dist_infection)

		self.champ_dist_infection.currentIndexChanged.connect(self.champ_dist_infection.changement_valeur)
		self.label_dist_infection.setToolTip("La distance de contagion de la maladie")

	def gerer_affichage_distance_contagion(self):
		if self.afficher_distance_infection.isChecked():
			self.sa_fenetre.sa_grille.afficher_distance_contagion = True
		else : 
			self.sa_fenetre.sa_grille.afficher_distance_contagion = False
