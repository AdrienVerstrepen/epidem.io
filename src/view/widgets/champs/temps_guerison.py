from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..parametres import Parametres

class Champ_temps_guerison(QComboBox):
	"""
	Liste déroulante permettant de sélectionner la durée d'infection de la maladie.

	Hérite de QComboBox et propose quatre options : Incurable, Courte, Moyenne, Longue.
	Chaque option correspond à une valeur numérique récupérable via un dictionnaire.
	"""
	son_menu : "Parametres"
	"""Référence au menu des paramètres."""
	
	son_texte : "str"
	"""Intitulé affiché dans le label associé."""
	
	changement_valeur : "None"
	"""Déclenchée lors d'un changement d'option, affiche en console la valeur correspondante."""
	
	recuperer_valeur_depuis_champ : "int"
	"""Retourne la valeur numérique associée à l'option sélectionnée."""
	def __init__(self, menu:"Parametres", nom:str) -> "Champ_temps_guerison":
		"""
		Le constructeur du champ permettant de choisir 
		les différents temps de guérison
		
		:param menu: Son composant parent
		:type menu: "Parametres"
		:param nom: Son nom
		:type nom: str
		:return: Le Champ_temps_guerison instancié
		:rtype: Champ_temps_guerison
		"""
		super().__init__()

		self.son_menu = menu
		self.son_texte = nom

		self.addItem("Incurable")
		self.addItem("Courte")
		self.addItem("Moyenne")
		self.addItem("Longue")

	def changement_valeur(self) -> None:
		"""
		Méthode pour mettre à jour
		la valeur choisie avec la valeur
		affichée
		"""
		self.setCurrentIndex(self.currentIndex())

	def recuperer_valeur_depuis_champ(self) -> int:
		"""Méthode pour récupérer la valeur"""
		return valeurs_possibles[self.currentText()]

	def changer_valeur(self, valeur) -> None:
		"""Méthode pour changer la valeur"""
		index = self.findText(valeur)
		self.setCurrentIndex(index)

valeurs_possibles = {
	"Incurable": -1,
	"Courte": 25,
	"Moyenne": 100,
	"Longue": 250
}
"""La traduction des valeurs possibles avec les valeurs affichées"""