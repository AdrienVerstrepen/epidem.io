from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Slider_transmission(QSlider):
	def __init__(self, menu:"Parametres", texte: str):
		super().__init__(Qt.Orientation.Horizontal)

		self.setMinimum(1)
		self.setMaximum(100)
		self.texte = texte
		self.son_menu = menu

	def changement_valeur(self):
		self.son_menu.label_transmission.setText(f"{self.texte} : {self.son_menu.slider_transmission.value()}%")

	def slider_relache(self):
		print(self.value())