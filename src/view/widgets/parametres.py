from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Parametres(QWidget):
	def __init__(self, ):
		super().__init__()
		layout = QVBoxLayout()
		self.setLayout(layout)

		layout.addWidget(QLabel("Paramètre 1"))
		layout.addWidget(QSlider())

		layout.addWidget(QLabel("Paramètre 2"))
		layout.addWidget(QLineEdit())

		layout.addStretch()
