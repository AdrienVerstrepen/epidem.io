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

    Attributs :
        texte (str): Le texte affiché dans le label associé.
        son_menu (Parametres): Référence au composant Parametres, utilisé pour
                               mettre à jour son label correspondant.

    Méthodes :
        changement_valeur (None): Met à jour le QLabel associé en affichant 
                                  la valeur actuelle du slider en pourcentage.
	"""
	def __init__(self, menu:"Parametres", texte: str):
		super().__init__(Qt.Orientation.Horizontal)

		self.setMinimum(1)
		self.setMaximum(100)
		self.texte = texte
		self.son_menu = menu

	def changement_valeur(self):
		self.son_menu.label_immunodeprime.setText(f"{self.texte} : {self.son_menu.champ_immunodeprime.value()}%")