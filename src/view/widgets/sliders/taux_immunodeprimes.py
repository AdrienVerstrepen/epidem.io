from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Slider_immunodeprime(QSlider):
    """
    Slider permettant de sélectionner le pourcentage de personnes immunodéprimées.

    Hérite de QSlider, orienté horizontalement, et met à jour dynamiquement
    le label associé dans le menu des paramètres.
    """
    texte : "str"
    """Le texte affiché dans le label associé."""
    
    son_menu : "Parametres"
    """Référence au composant Parametres, utilisé pour mettre à jour son label correspondant."""
    
    def __init__(self, menu:"Parametres", texte: str) -> "Slider_immunodeprime" :
        """
		Constructeur du composant à glisser pour 
		connaitre le pourcentage de personnes 
		immunodeprimees
		
		:param menu: Le composant parent
		:type menu: "Parametres"
		:param texte: Le texte à afficher
		:type texte: str
		:return: Le slider_immunodeprimes instancié
		:rtype: Slider_immunodeprimes
		"""
        super().__init__(Qt.Orientation.Horizontal)

        self.setMinimum(0)
        self.setMaximum(100)
        self.texte = texte
        self.son_menu = menu

    def changement_valeur(self) -> None:
        """
		Méthode qui change la valeur du label en fonction
		de la valeur du slider
		"""
        self.son_menu.label_immunodeprime.setText(f"{self.texte} : {self.son_menu.champ_immunodeprime.value()}%")