from PySide6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..barre_boutons import Barre_boutons

class Bouton_reinitialiser(QPushButton):
	def __init__(self, sa_barre : "Barre_boutons", texte: str):
		super().__init__()
		self.text = texte
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)

	def appui(self):
		self.sa_barre.get_bouton_demarrer().reinitialiser_etat()
		self.sa_barre.get_bouton_pause().reinitialiser_etat()
		self.sa_barre.sa_fenetre.sa_grille.reinitialiser_simulation()