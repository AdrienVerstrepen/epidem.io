from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Slider_transmission(QSlider):
	"""
    Slider permettant de définir le pourcentage de transmission de la maladie.

    Hérite de QSlider, orienté horizontalement, et met à jour en temps réel
    le label associé dans le menu Parametres selon la valeur sélectionnée.

    Attributs :
        texte (str): Texte affiché dans le label associé.
        son_menu (Parametres): Référence au composant Parametres pour modifier 
                               dynamiquement le label correspondant.

    Méthodes :
        changement_valeur (None): Met à jour le QLabel associé pour afficher
                                  la valeur actuelle du taux de transmission en pourcentage.
    """
	def __init__(self, menu:"Parametres", texte: str):
		super().__init__(Qt.Orientation.Horizontal)

		self.setMinimum(1)
		self.setMaximum(100)
		self.texte = texte
		self.son_menu = menu

	def changement_valeur(self):
		self.son_menu.label_transmission.setText(f"{self.texte} : {self.son_menu.slider_transmission.value()}%")