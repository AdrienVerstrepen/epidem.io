from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Taux_letalite(QSlider):
	def __init__(self, parent:QWidget):
		super().__init__(Qt.Orientation.Horizontal)

		self.parent = parent

	def changement_valeur(self):
		self.parent.label_letalite.setText(f"Value: {self.parent.slider_letalite.value()+1}")

	def slider_selectionne(self):
		print("Taux letalite choisi")

	def slider_relache(self):
		print("Taux letalite relaché")
	def slider_deplace(self, position):
		print(f"Valeur déplacée à : {position}")