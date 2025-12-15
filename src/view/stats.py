from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ..algorithmie import *
from pyqtgraph import *
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from ..algorithmie.simulation import *

matplotlib.use("Qt5Agg")

class Fenetre_statistiques(QWidget):
	def __init__(self, simu: "Simulation"):
		super().__init__()
		self.setWindowTitle("épidém.io - statistiques")
		self.simu = simu

		self.son_graphique = Figure(figsize=(5, 4), dpi=100)
		self.ses_axes = self.son_graphique.add_subplot(111)
		self.ses_axes.set_title("Evolution du nombre de personnes mortes au fil du temps")
		self.ses_axes.set_xlabel("Nombre d'itérations")
		
		self.ses_axes.set_ylabel("Nombre de morts en pourcentage")
		if simu:
			df = (simu.df_historique["nb_morts"] / simu.df_historique["nb_total"]) * 100
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
		if (self.isActiveWindow()): 
			self.ses_axes.clear()
			self.ses_axes.set_title("Evolution du nombre de personnes mortes au fil du temps")
			self.ses_axes.set_xlabel("Nombre d'itérations")
			self.ses_axes.set_ylabel("Nombre de morts en pourcentage")
			df = (self.simu.df_historique["nb_morts"] / self.simu.df_historique["nb_total"]) * 100
			self.ses_axes.plot(df)
			self.son_widget_graphique.draw()
			self.ses_axes.set_ylim(0, 100)