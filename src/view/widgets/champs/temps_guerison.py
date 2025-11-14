from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Champ_temps_guerison(QDateTimeEdit):
	def __init__(self, parent:QWidget):
		super().__init__(Qt.Orientation.Horizontal)

