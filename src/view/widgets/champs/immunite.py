from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..parametres import Parametres

class Champ_immunite(QCheckBox):
	"""
	Case à cocher définissant si l'immunité est activée après guérison.

	Hérite de QCheckBox et permet de notifier le menu des paramètres lors d'un changement d'état.
	"""
	son_texte : "str"
	"""Texte affiché dans le label associé."""
	
	son_menu : "Parametres"
	"""Référence au composant Parametres, permettant de mettre à jour son label correspondant."""

	def __init__(self, menu:"Parametres", nom: str) -> "Champ_immunite":
		"""
		Le constructeur du champ permettant de choisir 
		si l'immunité est active ou non
		
		:param menu: Son composant parent
		:type menu: "Parametres"
		:param nom: Son nom
		:type nom: str
		:return: Le Champ_immunite instancié
		:rtype: Champ_immunite
		"""
		super().__init__()

		self.son_texte = nom
		self.son_menu = menu
		self.setText(f"{nom}")

	def changer_valeur(self, valeur) -> None:
		"""
		Méthode qui change l'état visuel de la case 
		à cocher en fonction de sa valeur
		"""
		self.setChecked(valeur)