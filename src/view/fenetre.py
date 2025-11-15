from PySide6.QtWidgets import *
from PySide6.QtCore import *
from .widgets.grille import Grille_visualisation
from .widgets.parametres import Parametres
from .widgets.barre_boutons import Barre_boutons

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .widgets.parametres import Parametres

class Fenetre(QMainWindow):
	def __init__(self, nb_personnes: int, taille_fenetre: dict):
		super().__init__()
		self.setWindowTitle("épidém.io")

		self.largeur = taille_fenetre["largeur"]
		self.hauteur = taille_fenetre["hauteur"]
		self.nb_personnes = nb_personnes
		self.taille_fenetre = taille_fenetre

		self.resize(self.largeur, self.hauteur)

		widget_central = QWidget()
		self.setCentralWidget(widget_central)

		self.disposition_principale = QHBoxLayout()

		self.ses_parametres = Parametres(self)
		self.sa_grille = Grille_visualisation(taille_fenetre, nb_personnes, self)
		
		self.disposition_principale.addWidget(self.sa_grille, stretch=3)
		self.disposition_principale.addWidget(self.ses_parametres, stretch=1)

		self.boutons_haut = Barre_boutons(self)
		disposition_haut = QVBoxLayout()
		disposition_haut.addWidget(self.boutons_haut)
		disposition_haut.addLayout(self.disposition_principale)

		widget_central.setLayout(disposition_haut)