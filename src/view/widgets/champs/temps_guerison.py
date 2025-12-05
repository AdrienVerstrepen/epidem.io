from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Champ_temps_guerison(QComboBox):
	"""
    Liste déroulante permettant de sélectionner la durée d'infection de la maladie.

    Hérite de QComboBox et propose quatre options Incurable, Courte, Moyenne, Longue

    Chaque option correspond à une valeur numérique récupérable via un dictionnaire.

    Attributs :
        son_menu (Parametres): Référence au menu des paramètres.
        son_texte (str): Intitulé affiché dans le label associé.

    Méthodes :
        changement_valeur (None): Déclenchée lors d'un changement d'option,
                                  affiche en console la valeur correspondante.
        recuperer_valeur_depuis_champ () -> int:
            Retourne la valeur numérique associée à l'option sélectionnée.
    """
	def __init__(self, menu:"Parametres", nom:str):
		super().__init__()

		self.son_menu = menu
		self.son_texte = nom

		self.addItem("Incurable")
		self.addItem("Courte")
		self.addItem("Moyenne")
		self.addItem("Longue")
		self.setCurrentIndex(2)

	def changement_valeur(self):
		print(self.recuperer_valeur_depuis_champ())
		self.setCurrentIndex(self.currentIndex())

	def recuperer_valeur_depuis_champ(self) -> int:
		return valeurs_possibles[self.currentText()]
	
valeurs_possibles = {
    "Incurable": -1,
    "Courte": 5,
    "Moyenne": 20,
    "Longue": 50
}