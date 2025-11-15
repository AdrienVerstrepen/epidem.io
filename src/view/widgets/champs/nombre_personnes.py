from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Champ_nb_personnes(QSpinBox):
	def __init__(self, menu:Parametres, nom: str):
		super().__init__()

		self.setMinimum(1)
		self.setMaximum(100)

		self.son_texte = nom
		self.son_menu = menu

	def changement_valeur(self):
		self.son_menu.label_nb_personnes.setText(f"{self.son_texte} : {self.son_menu.champ_nb_personnes.value()}")