from PySide6.QtWidgets import QPushButton

class Bouton_mettre_en_pause(QPushButton):
	def __init__(self, sa_barre, texte):
		super().__init__()
		self.text = texte
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)
		self.etat = "continuer"

	def appui(self):
		if (self.etat == "continuer"):
			self.sa_barre.sa_fenetre.sa_grille.mettre_en_pause_simulation(True)
			self.etat = "en_pause"
			self.setText("Reprendre")
		else :
			self.sa_barre.sa_fenetre.sa_grille.mettre_en_pause_simulation(False)
			self.etat = "continuer"
			self.setText(self.text)
