from PySide6.QtWidgets import QPushButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..barre_boutons import Barre_boutons

class Bouton_reinitialiser(QPushButton):
	"""
    Bouton permettant de réinitialiser complètement l'état de la simulation.

    Hérite de QPushButton et déclenche la réinitialisation de l'état du bouton démarrer, 
	de l'état du bouton pause et de la simulation affichée dans la grille

    Attributs :
        sa_barre (Barre_boutons): La barre de boutons parente contenant les actions de contrôle.
        text (str): Le texte affiché sur le bouton.

    Méthodes :
        appui (None): Appelée lors de l'appui sur le bouton. Réinitialise les composants
                      liés au démarrage, à la pause et réinitialise la simulation graphique.
    """
	def __init__(self, sa_barre : "Barre_boutons", texte: str):
		super().__init__()
		self.text = texte
		self.setText(texte)
		self.sa_barre = sa_barre
		self.pressed.connect(self.appui)

	def appui(self):
		self.sa_barre.get_bouton_demarrer().reinitialiser_etat()
		self.sa_barre.get_bouton_pause().reinitialiser_etat()
		self.sa_barre.sa_fenetre.sa_grille.reinitialiser_simulation()