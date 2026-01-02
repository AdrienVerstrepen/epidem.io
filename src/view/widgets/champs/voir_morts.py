from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..parametres import Parametres

class Champ_voir_morts(QCheckBox):
	"""
	Case à cocher définissant si l'immunité est activée après guérison.

	Hérite de QCheckBox et permet d'activer ou non l'immunité.
	"""
	son_texte : "str"
	"""Texte affiché dans le label associé."""
	
	son_menu : "Parametres"
	"""Référence au composant Parametres, 
	permettant de mettre à jour son label correspondant."""
	
	changement_valeur : "None"
	"""Met à jour visuellement la case à cocher lors d'un changement d'état."""
	def __init__(self, menu:"Parametres", nom: str) -> "Champ_voir_morts":
		"""
		Constructeur de la classe Champ_voir_morts
	
		:param menu: Son composant parent
		:type menu: "Parametres"
		:param nom: Le nom du composant
		:type nom: str
		:return: Le Champ_voir_morts associé
		:rtype: Champ_voir_morts
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