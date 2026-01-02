from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Champ_taux_letalite(QDoubleSpinBox):
    """
    Champ numérique permettant de définir le nombre total de personnes
    présentes au lancement de la simulation.

    Hérite de QDoubleSpinBox et restreint la saisie entre 0 et 100,
    puis met à jour dynamiquement le label associé dans le menu Parametres.
    """
    son_texte : "str"
    """Texte de base affiché dans le label associé."""
    
    son_menu : "Parametres"
    """Référence au menu des paramètres permettant d'accéder et de modifier le label correspondant."""
    
    changement_valeur : "None"
    """Met à jour le QLabel associé pour afficher la nouvelle valeur du nombre de personnes."""
    def __init__(self, menu:"Parametres", nom: str) -> "Champ_taux_letalite":
        """
		Le constructeur du champ permettant de choisir 
		le taux de létalité souhaité
		
		:param menu: Son composant parent
		:type menu: "Parametres"
		:param nom: Son nom
		:type nom: str
		:return: Le Champ_taux_letalite instancié
		:rtype: Champ_taux_letalite
		"""
        super().__init__()

        self.setMinimum(0)
        self.setMaximum(100)

        self.son_texte = nom
        self.son_menu = menu
        self.setDecimals(5)
        self.setSingleStep(0.00001)

    def changement_valeur(self) -> None:
        """Méthode permettant d'afficher la valeur choisie
		dans le label"""
        self.son_menu.label_letalite.setText(f"{self.son_texte} : {round(self.son_menu.champ_letalite.value(),5)}%")