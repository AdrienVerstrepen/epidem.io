from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys
from view.widgets.grille import Grille_visualisation
from view.widgets.parametres import Parametres
from view.widgets.barre_boutons import Barre_boutons

class Fenetre(QMainWindow):
	def __init__(self):
		super().__init__()
		# Gestion titre et taille de la fenêtre
		self.setWindowTitle("épidém.io")

		self.largeur = 800
		self.hauteur = 600
		
		self.resize(self.largeur, self.hauteur)

		widget_central = QWidget()
		self.setCentralWidget(widget_central)

		disposition_principal = QHBoxLayout()

		taille_fenetre = [self.largeur, self.hauteur]

		self.widget_grille = Grille_visualisation(taille_fenetre)
		self.widget_parametres = Parametres()

		disposition_principal.addWidget(self.widget_grille, stretch=3)
		disposition_principal.addWidget(self.widget_parametres, stretch=1)

		self.boutons_haut = Barre_boutons()
		disposition_haut = QVBoxLayout()
		disposition_haut.addWidget(self.boutons_haut)
		disposition_haut.addLayout(disposition_principal)

		widget_central.setLayout(disposition_haut)
	