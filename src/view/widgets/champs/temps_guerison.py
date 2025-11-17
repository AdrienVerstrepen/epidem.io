from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Champ_temps_guerison(QComboBox):
	def __init__(self, menu:Parametres, nom:str):
		super().__init__()

		self.son_menu = menu
		self.son_texte = nom

		self.addItem("Incurable")
		self.addItem("Courte")
		self.addItem("Moyenne")
		self.addItem("Longue")

	def changement_valeur(self):
		print(self.recuperer_valeur_depuis_champ())

	def recuperer_valeur_depuis_champ(self) -> int:
		return valeurs_possibles[self.currentText()]

valeurs_possibles = {
    "Incurable": -1,
    "Courte": 5,
    "Moyenne": 20,
    "Longue": 50
}