from PySide6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..barre_boutons import Barre_boutons

class Bouton_demarrer(QPushButton):
	"""
	Bouton permettant de démarrer la simulation.

	Hérite de QPushButton et bascule son état entre actif et inactif.
	"""
	sa_barre : "Barre_boutons"
	"""La barre de boutons parente contenant les contrôles."""
	
	texte : "str"
	"""Libellé de base affiché lorsque la simulation n'est pas en pause."""
	
	son_style : "str"
	"""Le style actuel du bouton"""
	def __init__(self, sa_barre : "Barre_boutons", texte: str) -> "Bouton_demarrer":
		"""
		Constructeur du Bouton de démarrage
		
		:param sa_barre: Son composant parent
		:type sa_barre: "Barre_boutons"
		:param texte: Son texte
		:type texte: str
		:return: Le composant Bouton_demarrer instancié
		:rtype: Bouton_demarrer
		"""
		super().__init__()
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)
		self.son_style = self.styleSheet()

	def appui(self) -> None:
		"""Activation de la simulation et mise en
		mode désactivé du bouton démarrer"""
		self.sa_barre.sa_fenetre.sa_grille.demarrer_simulation()
		self.setEnabled(False)
		self.setStyleSheet("background-color: #999999; color: #eeeeee")
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setEnabled(True)
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setStyleSheet(self.son_style)

	def reinitialiser_etat(self) -> None:
		"""Restaure l'état par défaut du bouton 
		actif et remet le style initial."""
		self.setEnabled(True)
		self.setStyleSheet(self.son_style)
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setEnabled(False)
		self.sa_barre.sa_fenetre.bouton_fenetre_enfant.setStyleSheet("background-color: #999999; color: #eeeeee")