import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from src.view.fenetre import Fenetre

def main():
    application = QApplication()
    largeur = 900
    hauteur = 725
    taille_fenetre = {"largeur": largeur,"hauteur": hauteur}
    presenter_application()
    ihm = Fenetre(taille_fenetre)
    ihm.showMaximized()
    sys.exit(application.exec())

def presenter_application():
    """
    Cette fonctionne affiche une boîte modale
    qui bloque la suite du lancement de l'application
    pour permettre à l'utilisateur de prendre le temps 
    de bien lire et comprendre l'introduction du
    logiciel
    """
    dialogue = QMessageBox()
    dialogue.setWindowTitle("Explications")
    dialogue.setText("""
        <h1 align="center">Bienvenue sur <b>Epidem.io</b></h1>
        <p>
            Cette application vous permet de suivre la propagation d'une épidémie 
            au sein d'une population humaine en fonction de différents paramètres.
        </p>
        <p>
            Chaque personne est représentée par un point. Au cours de la simulation, la couleur de ces points 
            sera susceptible de changer car elle représente l'état actuel de la personne.
        </p>
        <p>
            Les différents états sont les suivants : 
        </p>
        <ul>
            <li>Les points verts indiquent les personnes en bonne santé.</li>
            <li>Les points jaunes symbolisent les personnes infectées.</li>
            <li>Les points rouges représentent les personnes décédées.</li>
            <li>Les points bleus illustrent les personnes immunisées.</li>
        </ul>
        <p>
            Les simulations lancées par l'utilisateur sont paramétrables.
            Une fois dans l'interface principale, vous aurez deux sections : 
            l'une dont les changements ne seront pris en compte qu'au lancement d'une 
            simulation ; l'autre où les changements sont pris en compte 
            instantanément.
        </p>
        <p>
            Enfin, certaines personnes sont représentées par des étoiles : ce sont les médecins. 
            Leur rôle est d'accélérer la guérison des personnes proches d'eux.
        </p>
    """)
    button = dialogue.exec()

if __name__ == "__main__":
    main()