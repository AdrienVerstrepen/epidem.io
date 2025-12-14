from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..parametres import Parametres

class Champ_immunite(QCheckBox):
	"""
	Case à cocher définissant si l'immunité est activée après guérison.

	Hérite de QCheckBox et permet de notifier le menu des paramètres lors d'un changement d'état.

	Attributs :
		son_texte (str): Texte affiché dans le label associé.
		son_menu (Parametres): Référence au composant Parametres, permettant
							   de mettre à jour son label correspondant.

	Méthodes :
		changement_valeur (None): Met à jour le QLabel associé lorsque la case est cochée
								  ou décochée. Affiche dans le label la valeur issue du
								  champ du nombre de personnes (comportement actuel du code).
	"""
	def __init__(self, menu:"Parametres", nom: str):
		super().__init__()

		self.son_texte = nom
		self.son_menu = menu

	def changement_valeur(self):
		self.son_menu.label_immunite.setText(f"{self.son_texte} : {self.son_menu.champ_immunite.isChecked()}")
		
	def changer_valeur(self, valeur):
		self.setChecked(valeur)