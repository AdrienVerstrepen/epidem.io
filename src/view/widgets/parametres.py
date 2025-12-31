from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from .sliders.taux_letalite import Slider_letalite
from .sliders.taux_transmission import Slider_transmission
from .sliders.taux_immunodeprimes import Slider_immunodeprime
from .sliders.taux_infectes import Slider_infectes
from .champs.nombre_personnes import Champ_nb_personnes
from .champs.temps_guerison import Champ_temps_guerison
from .champs.immunite import Champ_immunite
from .champs.natalite import Champ_taux_natalite
from .champs.letalite import Champ_taux_letalite
from .champs.distance_infection import Champ_distance_infection
from .champs.voir_morts import Champ_voir_morts

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..fenetre import Fenetre

import src.ressources_rc

class Parametres(QGroupBox):
	"""
	Composant graphique portant les champs de saisi des paramètres
	modifiables par l'utilisateur

	Hérite de QGroupBox et instancie les champs et leurs labels associés

	Attributs: 
		sa_fenetre (Fenetre): son objet parent Fenetre
		sa_disposition (QVBoxLayout): le layout suivi par ses composants
		label_letalite (QLabel): Le QLabel associé au slider letalite
		champ_letalite (Slider_letalite): Le composant à glisser permettant de récupérer la valeur pour le taux de létalité
		label_infectes (QLabel): Le QLabel associé au slider infectés
		champ_infectes (Slider_infectes): Composant permettant de récupérer la valeur du taux de personnes infectés
		label_transmission (QLabel): Le QLabel associé au slider transmissio
		champ_transmission (Slider_transmission): Composant récupérant la valeur du taux de transmission de la maladie
		label_immunodeprime (QLabel): QLabel associé au slider immunodéprimé
		champ_immunodeprime (Slider_immunodeprime): Composant récupérant la valeur du taux de personne immunodéprimés de la maladie
		label_nb_personnes (QLabel): QLabel associé au champ du nombre de personnes
		champ_nb_personnes (Champ_nb_personnes): Composant récupérant la valeur du nombre de personnes
		label_temps_guerison (QLabel): QLabel associé au champ du temps de guérison
		champ_temps_guerison (Champ_temps_guerison): Composant récupérant la valeur du temps de guérison de la maladie
		label_immunite (QLabel): QLabel associé au champ activant ou non l'immunité après guérison
		champ_immunite (Champ_immunite): Composant récupérant la possibilté ou non d'avoir une immunité

	Méthodes:
		initialiser_parametres (None): fonction auxiliaire qui initialie tous les composants
		initialiser_composant (None): 
	"""
	def __init__(self, fenetre: "Fenetre"):
		super().__init__()

		self.sa_fenetre = fenetre
		self.sa_disposition = QVBoxLayout()
		self.setLayout(self.sa_disposition)

		self.groupement_non_instantane = QGroupBox("Paramètres non instantanés", self)
		self.groupement_instantane = QGroupBox("Paramètres instantanés", self)

		self.sa_disposition.addWidget(self.groupement_non_instantane)
		self.sa_disposition.addWidget(self.groupement_instantane)

		self.layout_non_instantane = QVBoxLayout()
		self.layout_instantane = QVBoxLayout()

		self.groupement_non_instantane.setLayout(self.layout_non_instantane)
		self.groupement_instantane.setLayout(self.layout_instantane)
		self.initialiser_parametres()
		
		self.composant_distance_infection = QWidget()
		self.afficher_distance_infection = QCheckBox("Afficher la distance d'infection", self)
		self.afficher_distance_infection.stateChanged.connect(self.gerer_affichage_distance_contagion)
		arrangement_distance_infection = QVBoxLayout()
		arrangement_distance_infection.addWidget(self.afficher_distance_infection)
		self.composant_distance_infection.setLayout(arrangement_distance_infection)
		
		self.layout_instantane.addWidget(self.composant_distance_infection)
		self.sa_disposition.addStretch()
		

	def initialiser_composant(self, nom, texte: str, valeur_defaut: int, unite : str, classe : type[QWidget], tooltip : str, instantane : int = 0):
		
		composant = QWidget()
		arrangement_principal = QVBoxLayout()
		arrangement_label_icone = QHBoxLayout()
		champ = classe(self, texte)
		if not (isinstance(champ, Champ_immunite) or isinstance(champ, Champ_voir_morts)):
			label = QLabel(f"{texte} : {valeur_defaut}{unite}")
			setattr(self, f"label_{nom}", label)
			arrangement_label_icone.addWidget(label)
			icone = QLabel()
			pix = QPixmap(":/icons/tooltip.png").scaled(
				16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation
			)
			icone.setPixmap(pix)
			arrangement_label_icone.addStretch(1)
			arrangement_label_icone.addWidget(icone)
			arrangement_principal.addLayout(arrangement_label_icone)
		setattr(self, f"champ_{nom}", champ)
		arrangement_principal.addWidget(champ)
		
		if isinstance(champ, Champ_temps_guerison) or isinstance(champ, Champ_distance_infection):
			getattr(self, f"champ_{nom}").changer_valeur(valeur_defaut)
			champ.currentIndexChanged.connect(champ.changement_valeur)
			icone.setToolTip(tooltip)
		elif isinstance(champ, Champ_immunite) or isinstance(champ, Champ_voir_morts):
			getattr(self, f"champ_{nom}").changer_valeur(valeur_defaut)
			# champ.stateChanged.connect(champ.changement_valeur)
		else:
			getattr(self, f"champ_{nom}").setValue(valeur_defaut)
			champ.valueChanged.connect(champ.changement_valeur)
			icone.setToolTip(tooltip)
		composant.setLayout(arrangement_principal)
		if instantane != 0:
			self.layout_instantane.addWidget(composant)
		else:
			self.layout_non_instantane.addWidget(composant)

	def initialiser_parametres(self):
		# letalite
		self.initialiser_composant(
			"letalite", 
			"Taux de létalité de la maladie",
			3.5,
			"%",
			Champ_taux_letalite,
			"Le pourcentage de risque qu'une personne décède de la maladie"
		)
		# nb_personnes
		self.initialiser_composant(
			"nb_personnes", 
			"Effectif de la population",
			100,
			"",
			Champ_nb_personnes,
			"Le nombre de personnes présentes au lancement de la simulation"
		)
		# transmission
		self.initialiser_composant(
			"transmission", 
			"Pourcentage de transmission de la maladie",
			20,
			"%",
			Slider_transmission,
			"La probabilité qu'une personne infectée transmette la maladie à une autre"
		)
		# immunodeprimés
		self.initialiser_composant(
			"immunodeprime", 
			"Pourcentage de personnes immunodéprimées",
			15,
			"%",
			Slider_immunodeprime,
			"Le pourcentage de personnes immunodéprimées au lancement de la simulation (les personnes immunodéprimées sont notamment les personnes âgées)"
		)
		# infectés
		self.initialiser_composant(
			"infectes", 
			'Pourcentage de patient(s) "0"',
			4,
			"%",
			Slider_infectes,
			"Le pourcentage de personnes infectées au lancement de la simulation"
		)
		# temps_guerison
		self.initialiser_composant(
			"temps_guerison", 
			"Duree d'infection de la maladie",
			"Moyenne",
			"",
			Champ_temps_guerison,
			"Le temps pour guérir de la maladie"
		)
		# natalite
		self.initialiser_composant(
			"natalite",
			"Taux de natalité",
			2,
			"%",
			Champ_taux_natalite,
			"Le taux de natalité au sein de la population"
		)
		# distance_infection
		self.initialiser_composant(
			"distance_infection",
			"Distance de contagion de la maladie",
			"Moyenne",
			"",
			Champ_distance_infection,
			"La distance nécessaire entre chaque personne pour qu'il y ait une chance de tranmsission de la maladie"
		)
		# immunité
		self.initialiser_composant(
			"immunite", 
			"Immunité après guérison",
			False,
			"",
			Champ_immunite,
			"La possibilité ou non d'être immunisé après avoir guéri de la maladie"
		)

		self.initialiser_composant(
			"morts_visibles",
			"Voir les morts",
			False,
			"",
			Champ_voir_morts,
			"Si activé, toutes les personnes mortes sont conservées dans l'interface.\n Si désactivé, elles seront retirées progressivement",
			instantane=1
		)

	def gerer_affichage_distance_contagion(self):
		if self.afficher_distance_infection.isChecked():
			self.sa_fenetre.sa_grille.afficher_distance_contagion = True
		else : 
			self.sa_fenetre.sa_grille.afficher_distance_contagion = False
