from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ..classes import *
from pyqtgraph import *
import time
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .fenetre import Fenetre

class FenetreStats(QWidget):
	def __init__(self, simu):
		super().__init__()
		layout = QVBoxLayout()
		self.label = QLabel("Stats")
		layout.addWidget(self.label)
		graphique = PlotWidget()
		print(simu.df_historique)
		layout.addWidget(graphique)
		sains = simu.df_historique["nb_sains"]
		infectes = simu.df_historique["nb_infectes"]
		immunises = simu.df_historique["nb_immunises"]
		morts = simu.df_historique["nb_morts"]
		x = simu.df_historique.index
		graphique.plot(x, sains, pen=mkPen('g', width=2), name="S")
		graphique.plot(x, infectes, pen=mkPen('r', width=2), name="Inf")
		graphique.plot(x, immunises, pen=mkPen('b', width=2), name="Imm")
		graphique.plot(x, morts, pen=mkPen('k', width=2), name="Morts")

		self.setLayout(layout)