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
	def __init__(self, fenetre: "Fenetre"):
		super().__init__()

		self.sa_fenetre = fenetre
		self.sa_disposition = QVBoxLayout()
		self.setLayout(self.sa_disposition)

		self.initialiser_slider_letalite("Taux de létalité de la maladie", 35)

		self.initialiser_champ_nb_personnes("Effectif de la population", 20)

		self.initialiser_slider_transmission("Pourcentage de transmission", 50)
		
		self.initialiser_slider_immunodeprime("Pourcentage de personnes immunodéprimées", 50)

		self.initialiser_slider_infectes('Pourcentage de patient(s) "0"', 10)

		self.initialiser_champ_temps_guerison("Duree d'infection de la maladie", -1)

		self.initialiser_champ_immunite("Immunité après guérison", False)

		self.sa_disposition.addStretch()

	def initialiser_slider_letalite(self, nom: str, valeur_defaut: int):
		self.label_letalite = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_letalite)
		
		self.slider_letalite = Slider_letalite(self, nom)
		self.slider_letalite.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_letalite)

		self.slider_letalite.valueChanged.connect(self.slider_letalite.changement_valeur)
		self.slider_letalite.sliderReleased.connect(self.slider_letalite.slider_relache)

	def initialiser_slider_infectes(self, nom: str, valeur_defaut: int):
		self.label_infectes = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_infectes)
		
		self.slider_infectes = Slider_infectes(self, nom)
		self.slider_infectes.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_infectes)

		self.slider_infectes.valueChanged.connect(self.slider_infectes.changement_valeur)
		self.slider_infectes.sliderReleased.connect(self.slider_infectes.slider_relache)
	
	def initialiser_slider_transmission(self, nom: str, valeur_defaut: int):
		self.label_transmission = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_transmission)
		
		self.slider_transmission = Slider_transmission(self, nom)
		self.slider_transmission.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_transmission)

		self.slider_transmission.valueChanged.connect(self.slider_transmission.changement_valeur)
		self.slider_transmission.sliderReleased.connect(self.slider_transmission.slider_relache)

	def initialiser_slider_immunodeprime(self, nom: str, valeur_defaut: int):
		self.label_immunodeprime = QLabel(f"{nom} : {valeur_defaut}%")
		self.sa_disposition.addWidget(self.label_immunodeprime)
		
		self.slider_immunodeprime = Slider_immunodeprime(self, nom)
		self.slider_immunodeprime.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.slider_immunodeprime)

		self.slider_immunodeprime.valueChanged.connect(self.slider_immunodeprime.changement_valeur)
		self.slider_immunodeprime.sliderReleased.connect(self.slider_immunodeprime.slider_relache)

	def initialiser_champ_nb_personnes(self, nom: str, valeur_defaut: int):	
		self.label_nb_personnes = QLabel(f"{nom} : {valeur_defaut}")
		self.sa_disposition.addWidget(self.label_nb_personnes)

		self.champ_nb_personnes = Champ_nb_personnes(self, nom)
		self.champ_nb_personnes.setValue(valeur_defaut)
		self.sa_disposition.addWidget(self.champ_nb_personnes)

		self.champ_nb_personnes.valueChanged.connect(self.champ_nb_personnes.changement_valeur)

	def initialiser_champ_temps_guerison(self, nom: str, valeur_defaut: int):
		self.label_temps_guerison = QLabel(f"{nom} : ")
		self.sa_disposition.addWidget(self.label_temps_guerison)

		self.champ_temps_guerison = Champ_temps_guerison(self, nom)
		self.sa_disposition.addWidget(self.champ_temps_guerison)

		self.champ_temps_guerison.currentIndexChanged.connect(self.champ_temps_guerison.changement_valeur)

	def initialiser_champ_immunite(self, nom: str, valeur_defaut: int):
		self.label_immunite = QLabel(f"{nom} : {valeur_defaut}")
		self.sa_disposition.addWidget(self.label_immunite)

		self.champ_immunite = Champ_immunite(self, nom)
		self.sa_disposition.addWidget(self.champ_immunite)

		self.champ_immunite.stateChanged.connect(self.champ_immunite.changement_valeur)