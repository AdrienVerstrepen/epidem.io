from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Taux_letalite(QSlider):
	def __init__(self, parent:QWidget):
		super().__init__(Qt.Orientation.Horizontal)

		self.parent = parent

	def value_changed(self):
		self.parent.label_letalite.setText(f"Value: {self.parent.slider_letalite.value()+1}")

	def slider_pressed(self):
		print("Slider pressed")

	def slider_released(self):
		print("Slider released")
	def slider_moved(self, position):
		print(f"Slider moved to: {position}")