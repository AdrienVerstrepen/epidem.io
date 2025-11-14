from PySide6.QtWidgets import QPushButton

class Bouton_reinitialiser(QPushButton):
	def __init__(self, sa_barre, texte):
		super().__init__()
		self.text = texte
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)

	def appui(self):
		self.sa_barre.get_bouton_demarrer().reinitialiser_etat()
