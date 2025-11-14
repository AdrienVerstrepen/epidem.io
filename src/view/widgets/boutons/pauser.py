from PySide6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..barre_boutons import Barre_boutons

class Bouton_mettre_en_pause(QPushButton):
	def __init__(self, sa_barre: "Barre_boutons", texte : str):
		super().__init__()
		self.setText(texte)
		self.texte = texte
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)
		self.etat = "continuer"

	def appui(self):
		if not self.sa_barre.sa_fenetre.sa_grille.est_en_cours():
			return 
		if (self.etat == "continuer"):
			self.sa_barre.sa_fenetre.sa_grille.mettre_en_pause_simulation(True)
			self.etat = "en_pause"
			self.setText("Reprendre")
		else :
			self.sa_barre.sa_fenetre.sa_grille.mettre_en_pause_simulation(False)
			self.etat = "continuer"
			self.setText(self.texte)

	def reinitialiser_etat(self):
		self.etat = "continuer"
		self.setText(self.texte)