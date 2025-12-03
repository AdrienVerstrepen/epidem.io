from PySide6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..barre_boutons import Barre_boutons

class Bouton_mettre_en_pause(QPushButton):
	"""
    Bouton permettant de mettre en pause ou de reprendre la simulation.

    Hérite de QPushButton et bascule son état entre "continuer" et "en_pause" 

    Attributs :
        sa_barre (Barre_boutons): La barre de boutons parente contenant les contrôles.
        texte (str): Libellé de base affiché lorsque la simulation n'est pas en pause.
        etat (str): L'état actuel du bouton.

    Méthodes :
        appui (None): Gère l'appui sur le bouton. Met en pause ou reprend la simulation,
                      et modifie dynamiquement le texte du bouton.
        reinitialiser_etat (None): Restaure l'état par défaut du bouton ("continuer")
                                   et remet le texte initial.
    """
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