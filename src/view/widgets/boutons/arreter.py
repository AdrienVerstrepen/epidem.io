from PySide6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..barre_boutons import Barre_boutons

class Bouton_arreter(QPushButton):
	"""
	Bouton permettant d'arrêter la simulation.

	Hérite de QPushButton.
	"""
	sa_barre : "Barre_boutons"
	"""La barre de boutons parente contenant les contrôles."""
	
	texte : "str"
	"""Libellé de base affiché lorsque la simulation n'est pas en pause."""
	def __init__(self, sa_barre : "Barre_boutons", texte: str) -> "Bouton_arreter":
		"""
		Constructeur du Bouton d'arrêt
		
		:param sa_barre: Le composant parent
		:type sa_barre: "Barre_boutons"
		:param texte: Son texte
		:type texte: str
		:return: Le Bouton_arreter instancié
		:rtype: Bouton_arreter
		"""
		super().__init__()
		self.text = texte
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)

	def appui(self) -> None:
		"""Arrêt de la simulation
		lorsque le bouton est cliqué"""
		self.sa_barre.sa_fenetre.sa_grille.arreter_simulation()