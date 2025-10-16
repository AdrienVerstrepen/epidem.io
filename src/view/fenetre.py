from PySide6.QtWidgets import *
from PySide6.QtCore import *
import sys
from widgets.grille import Grille
from widgets.parametres import Parametres
from widgets.barre_boutons import Barre_boutons

class Fenetre(QMainWindow):
	def __init__(self):
		super().__init__()
		# Gestion titre et taille de la fenêtre
		self.setWindowTitle("épidém.io")
		self.resize(800, 600)
		
		widget_central = QWidget()
		self.setCentralWidget(widget_central)

		disposition_principal = QHBoxLayout()

		self.widget_grille = Grille()
		self.widget_parametres = Parametres()

		disposition_principal.addWidget(self.widget_grille, stretch=3)
		disposition_principal.addWidget(self.widget_parametres, stretch=1)

		self.boutons_haut = Barre_boutons()
		disposition_haut = QVBoxLayout()
		disposition_haut.addWidget(self.boutons_haut)
		disposition_haut.addLayout(disposition_principal)

		widget_central.setLayout(disposition_haut)
