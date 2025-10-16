from PySide6.QtWidgets import *
from PySide6.QtCore import *

class Barre_boutons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.buttons = []
        for i in range(4):
            btn = QPushButton(f"Bouton {i+1}")
            layout.addWidget(btn)
            self.buttons.append(btn)

        layout.addStretch()