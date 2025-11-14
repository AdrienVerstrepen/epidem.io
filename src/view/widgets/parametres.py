from PySide6.QtWidgets import *
from PySide6.QtCore import *
from .sliders.taux_letalite import Slider_letalite
from .sliders.taux_transmission import Slider_transmission
from .sliders.taux_infectes import Slider_infectes

class Parametres(QGroupBox):
	def __init__(self):
		super().__init__()

		self.sa_disposition = QVBoxLayout()
		self.setLayout(self.sa_disposition)

		# disposition.addWidget(QLabel("Valeur numérique 1"))
		# disposition.addWidget(QSpinBox())

		self.initialiser_slider_letalite("Taux de létalité de la maladie")
		# self.initialiser_slider_infectes("")
		# self.initialiser_slider_transmission("")
		# self.initialiser_champ_nb_personnes("")
		# self.initialiser_champ_temps_guerison("")

		self.sa_disposition.addStretch()

	def initialiser_slider_letalite(self, nom: str):
		self.label_letalite = QLabel(nom)
		self.sa_disposition.addWidget(self.label_letalite)
		self.slider_letalite = Slider_letalite(self, nom)
		self.sa_disposition.addWidget(self.slider_letalite)
		self.slider_letalite.valueChanged.connect(self.slider_letalite.changement_valeur)
		self.slider_letalite.sliderPressed.connect(self.slider_letalite.slider_selectionne)
		self.slider_letalite.sliderReleased.connect(self.slider_letalite.slider_relache)
		self.slider_letalite.sliderMoved.connect(self.slider_letalite.slider_deplace)

	# def initialiser_slider_infectes(self):

	# def initialiser_slider_transmission(self):

	# def initialiser_champ_nb_personnes(self):	

	# def initialiser_champ_temps_guerison(self):

