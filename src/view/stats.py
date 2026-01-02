from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ..algorithmie import *
from pyqtgraph import *
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .fenetre import Fenetre
	from ..algorithmie.simulation import *

matplotlib.use("Qt5Agg")

class Fenetre_statistiques(QWidget):
	"""
	Fenêtre secondaire de l'application.

	Cette classe hérite de :class:`QWidget` et s'occupe de
	porter le graphique représentant l'évolution du 
	nombre de morts au sein de la population.

	Attributs:
		sa_simulation (Simulation): La simulation courante
		son_graphique (Figure): Le graphique matplotlib
		ses_axes (Axes): les axes du graphique
		son_widget_graphique (FigureCanvasQTagg): Le composant Qt porteur du graphique
	
	Méthodes:
		rafraichir_graphique (None): Permet de mettre à jour le graphique
									 pour suivre l'évolution de la simulation
									 en temps réel
	"""
	def __init__(self, parent : "Fenetre", simulation: "Simulation"):
		super().__init__()
		self.setWindowTitle("épidém.io - statistiques")
		self.sa_simulation = simulation
		self.sa_fenetre_mere = parent

		self.son_graphique = Figure(figsize=(5, 4), dpi=100)
		self.ses_axes = self.son_graphique.add_subplot(111)
		self.ses_axes.set_title("Evolution du nombre de personnes mortes au fil du temps")
		self.ses_axes.set_xlabel("Nombre d'itérations")
		
		self.ses_axes.set_ylabel("Nombre de morts en pourcentage")
		if self.sa_simulation:
			df = (self.sa_simulation.df_historique["nb_morts"] / self.sa_simulation.df_historique["nb_total"]) * 100
			self.ses_axes.plot(df)

		self.ses_axes.set_ylim(0, 100)

		self.son_widget_graphique = FigureCanvasQTAgg(self.son_graphique)
		toolbar = NavigationToolbar(self.son_widget_graphique, self)

		parametre_voulu = "Save"
		for action in toolbar.actions():
			if action.text() != parametre_voulu:
				toolbar.removeAction(action)

		layout = QVBoxLayout()
		layout.addWidget(toolbar)
		layout.addWidget(self.son_widget_graphique)
		self.setLayout(layout)

		self.timer = QtCore.QTimer()
		self.timer.setInterval(500)
		self.timer.timeout.connect(self.rafraichir_graphique)
		self.timer.start()

		self.show()
		
	def rafraichir_graphique(self):
		if self.sa_fenetre_mere.sa_grille.sa_simulation != self.sa_simulation:
			self.sa_simulation = self.sa_fenetre_mere.sa_grille.sa_simulation
		if (self.isActiveWindow()):
			self.ses_axes.clear()
			self.ses_axes.set_title("Evolution du nombre de personnes mortes au fil du temps")
			self.ses_axes.set_xlabel("Nombre d'itérations")
			self.ses_axes.set_ylabel("Nombre de morts en pourcentage")
			df = (self.sa_simulation.df_historique["nb_morts"] / self.sa_simulation.df_historique["nb_total"]) * 100
			self.ses_axes.plot(df)
			self.ses_axes.set_ylim(0, 100)
			self.son_widget_graphique.draw()