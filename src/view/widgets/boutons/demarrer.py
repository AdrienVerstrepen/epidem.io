from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Slot

class Bouton_demarrer(QPushButton):
	def __init__(self, sa_barre, texte):
		super().__init__()
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)

	def appui(self):
		self.sa_barre.sa_fenetre.sa_grille.demarrer_simulation()
		self.setEnabled(False)
		self.setStyleSheet("background-color: #2b2b2b; color: #9d9d9d")