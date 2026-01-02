from PySide6.QtWidgets import *
from PySide6.QtCore import *
from .widgets.grille import Grille_visualisation
from .widgets.parametres import Parametres
from .widgets.barre_boutons import Barre_boutons

from typing import TYPE_CHECKING

from .stats import *

if TYPE_CHECKING:
    from .widgets.parametres import Parametres

class Fenetre(QMainWindow):
	"""
	Fenêtre principale de l'application.

	Cette classe hérite de :class:`QMainWindow` et s'occupe de l'assemblage 
	des différents éléments composants de l'interface. 

	Attributs:
		largeur (int): largeur de la fenêtre
		hauteur (int): hauteur de la fenêtre
		taille_fenetre (dict): le dictionnaire contenant la largeur et la hauteur
		disposition_principale (QHBoxLayout): disposition comportant les 3 sections de l'interface
		ses_parametres (Parametres): section comportant les paramètres modifiables par l'utilisateur
		sa_grille (Grille_visualisation): section comportant la représentation graphique de la simulation
		boutons_haut (Barre_boutons): section comportant les boutons permettant de gérer l'état de la simulation
	"""
	def __init__(self, taille_fenetre: dict):
		"""
		Constructeur de la classe Fenetre.

		Paramètres:
			taille_fenetre (dict): dictionnaire permettant l'accès par clé à la hauteur et la largeur souhaitée

		Retourne: 
			Fenetre: l'objet Fenetre initialisé avec ses 3 sections.
		"""
		super().__init__()
		self.setWindowTitle("épidém.io")
		self.sa_fenetre_enfant = None

		self.sa_largeur = taille_fenetre["largeur"]
		self.sa_hauteur = taille_fenetre["hauteur"]
		self.taille_fenetre = taille_fenetre

		self.resize(self.sa_largeur, self.sa_hauteur)

		widget_central = QWidget()
		self.setCentralWidget(widget_central)

		self.sa_disposition_principale = QHBoxLayout()

		self.ses_parametres = Parametres(self)
		parametres_defilables = QScrollArea()
		parametres_defilables.setWidget(self.ses_parametres)
		parametres_defilables.setWidgetResizable(True)
		parametres_defilables.setMinimumWidth(380)
		self.sa_grille = Grille_visualisation(self, taille_fenetre)
		
		self.sa_disposition_principale.addWidget(self.sa_grille, stretch=3)
		self.sa_disposition_principale.addWidget(parametres_defilables, stretch=1)

		self.son_menu = Barre_boutons(self)
		disposition_menu = QVBoxLayout()
		disposition_menu.addWidget(self.son_menu)
		disposition_menu.addLayout(self.sa_disposition_principale)
		widget_central.setLayout(disposition_menu)
		
		self.bouton_fenetre_enfant = QPushButton("Afficher les statistiques")
		self.bouton_fenetre_enfant.clicked.connect(self.ouvrir_fenetre)
		self.son_menu.sa_disposition.addWidget(self.bouton_fenetre_enfant, 0, 5)
		self.bouton_fenetre_enfant.setEnabled(False)
		self.style_bouton_fenetre_enfant = self.bouton_fenetre_enfant.styleSheet()
		self.bouton_fenetre_enfant.setStyleSheet("background-color: #999999; color: #eeeeee")

		self.setMinimumHeight(300)

	def ouvrir_fenetre(self, checked):
		if self.sa_fenetre_enfant is None:
			self.sa_fenetre_enfant = Fenetre_statistiques(self, self.sa_grille.sa_simulation)
		else:
			self.sa_fenetre_enfant.destroy()
			self.sa_fenetre_enfant = Fenetre_statistiques(self, self.sa_grille.sa_simulation)
		self.sa_fenetre_enfant.show()