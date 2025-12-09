from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Slider_letalite(QSlider):
	"""
    Slider permettant de définir le taux de létalité de la maladie.

    Hérite de QSlider, configuré horizontalement, et met à jour le label
    correspondant dans le panneau de paramètres à chaque modification.

    Attributs :
        texte (str): Intitulé affiché dans le label associé.
        son_menu (Parametres): Menu parent permettant la mise à jour du label lié.

    Méthodes :
        changement_valeur (None): Actualise le QLabel associé en affichant la
                                  valeur courante du taux de létalité en pourcentage.
    """
	def __init__(self, menu:"Parametres", texte: str):
		super().__init__(Qt.Orientation.Horizontal)

		self.setMinimum(1)
		self.setMaximum(100)
		self.texte = texte
		self.son_menu = menu

	def changement_valeur(self):
		self.son_menu.label_letalite.setText(f"{self.texte} : {self.son_menu.slider_letalite.value()}%")