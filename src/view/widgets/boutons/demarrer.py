from PySide6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..barre_boutons import Barre_boutons

class Bouton_demarrer(QPushButton):
	def __init__(self, sa_barre : "Barre_boutons", texte: str):
		super().__init__()
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)
		self.son_style = self.styleSheet()

	def appui(self):
		self.sa_barre.sa_fenetre.sa_grille.demarrer_simulation()
		self.setEnabled(False)
		self.setStyleSheet("background-color: #999999; color: #eeeeee")
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setEnabled(True)
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setStyleSheet(self.son_style)

	def reinitialiser_etat(self):
		self.setEnabled(True)
		self.setStyleSheet(self.son_style)
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setEnabled(False)
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setStyleSheet("background-color: #999999; color: #eeeeee")