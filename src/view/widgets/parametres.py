from PySide6.QtWidgets import *
from PySide6.QtCore import *
from view.widgets.sliders.taux_letalite import Taux_letalite

class Parametres(QWidget):
	def __init__(self):
		super().__init__()

		disposition = QVBoxLayout()
		self.setLayout(disposition)

		disposition.addWidget(QLabel("Valeur numérique 1"))
		disposition.addWidget(QSpinBox())

		self.label_letalite = QLabel("Valeur numérique flottante : 0")
		disposition.addWidget(self.label_letalite)
		self.slider_letalite = Taux_letalite(self)
		disposition.addWidget(self.slider_letalite)

		self.slider_letalite.valueChanged.connect(self.slider_letalite.changement_valeur)
		self.slider_letalite.sliderPressed.connect(self.slider_letalite.slider_selectionne)
		self.slider_letalite.sliderReleased.connect(self.slider_letalite.slider_relache)
		self.slider_letalite.sliderMoved.connect(self.slider_letalite.slider_deplace)

		disposition.addStretch()

