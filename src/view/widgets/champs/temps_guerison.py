from PySide6.QtWidgets import *
from PySide6.QtCore import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..parametres import Parametres

class Champ_temps_guerison(QComboBox):
	def __init__(self, menu:Parametres, nom:str):
		super().__init__()

		self.son_menu = menu
		self.son_texte = nom

