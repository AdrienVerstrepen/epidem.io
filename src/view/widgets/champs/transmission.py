from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Champ_taux_transmission(QDoubleSpinBox):
	"""
    Champ numérique permettant de définir le nombre total de personnes
    présentes au lancement de la simulation.

    Hérite de QDoubleSpinBox et restreint la saisie entre 1 et 100,
    puis met à jour dynamiquement le label associé dans le menu Parametres.

    Attributs :
        son_texte (str): Texte de base affiché dans le label associé.
        son_menu (Parametres): Référence au menu des paramètres permettant
                               d'accéder et de modifier le label correspondant.

    Méthodes :
        changement_valeur (None): Met à jour le QLabel associé pour afficher
                                  la nouvelle valeur du nombre de personnes.
    """
	def __init__(self, menu:"Parametres", nom: str):
		super().__init__()

		self.setMinimum(0)
		self.setMaximum(100)

		self.son_texte = nom
		self.son_menu = menu
		self.setDecimals(5)
		self.setSingleStep(0.00001)

	def changement_valeur(self):
		self.son_menu.label_transmission.setText(f"{self.son_texte} : {round(self.son_menu.champ_transmission.value(),5)}%")