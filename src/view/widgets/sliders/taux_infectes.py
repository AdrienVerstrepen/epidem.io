from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Slider_infectes(QSlider):
	"""
    Slider permettant de définir le pourcentage initial de personnes infectées

    Hérite de QSlider, orienté horizontalement, et met à jour le label associé
    dans le menu des paramètres en fonction de la valeur actuelle.

    Attributs :
        texte (str): Texte de base affiché dans le label associé.
        son_menu (Parametres): Référence au composant Parametres permettant
                               de modifier le label lié à ce slider.

    Méthodes :
        changement_valeur (None): Met à jour le QLabel associé en affichant
                                  la valeur actuelle du slider suivie d’un pourcentage.
    """
	def __init__(self, menu:"Parametres", texte: str):
		super().__init__(Qt.Orientation.Horizontal)

		self.setMinimum(1)
		self.setMaximum(100)
		self.texte = texte
		self.son_menu = menu

	def changement_valeur(self):
		self.son_menu.label_infectes.setText(f"{self.texte} : {self.son_menu.slider_infectes.value()}%")