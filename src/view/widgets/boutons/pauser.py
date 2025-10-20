from PySide6.QtWidgets import QPushButton

class Bouton_mettre_en_pause(QPushButton):
	def __init__(self, sa_barre, text):
		super().__init__()
		self.setText(text)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)

	def appui(self):
		self.sa_barre.sa_fenetre.sa_grille.pauser_simulation()
