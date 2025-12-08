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
	
	Méthodes:
		__init__ (Fenetre): constructeur
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

		self.w = None

		self.largeur = taille_fenetre["largeur"]
		self.hauteur = taille_fenetre["hauteur"]
		self.taille_fenetre = taille_fenetre

		self.resize(self.largeur, self.hauteur)

		widget_central = QWidget()
		self.setCentralWidget(widget_central)

		self.disposition_principale = QHBoxLayout()

		self.ses_parametres = Parametres(self)
		self.sa_grille = Grille_visualisation(self, taille_fenetre)
		
		self.disposition_principale.addWidget(self.sa_grille, stretch=3)
		self.disposition_principale.addWidget(self.ses_parametres, stretch=1)

		self.boutons_haut = Barre_boutons(self)
		disposition_haut = QVBoxLayout()
		disposition_haut.addWidget(self.boutons_haut)
		disposition_haut.addLayout(self.disposition_principale)

		widget_central.setLayout(disposition_haut)

		self.bouton = QPushButton("Stats")
		self.bouton.clicked.connect(self.show_other_window)
		self.ses_parametres.sa_disposition.addWidget(self.bouton)

	def show_other_window(self, checked):
		if self.w is None:
			self.w = FenetreStats(self.sa_grille.sa_simulation)
		else:
			self.w.destroy()
			self.w = FenetreStats(self.sa_grille.sa_simulation)
		self.w.show()