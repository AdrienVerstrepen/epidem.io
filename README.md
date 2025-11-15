# epidem.io

## Description du projet
Projet de simulation de propagation d'épidémie réalisé en python.

Adresse du dépôt git : https://github.com/AdrienVerstrepen/epidem.io

## Installation

## Fonctionnalités

## Organisation du projet

Le dossier doc contient les différents documents liés à la documentation du projet : 
* Cahier des charges
* Documentation
* Diagramme de classe
* Diagramme de Gantt
* Retroplanning

Le dossier src contient le code source du projet

Le dossier src/bin contient les binaires préconstruits et compilés avec [PyInstaller](url:https://pyinstaller.org/en/stable/index.html)

### Structure du projet

```
.gitignore
README.md
doc
   |-- cahier_des_charges.md
   |-- diagramme-de-classe-epidem.io.mdj
launch-app.sh
requirements.txt
src
   |-- __init__.py
   |-- classes.py
   |-- ihm.py
   |-- main.py
   |-- view
   |   |-- __init__.py
   |   |-- fenetre.py
   |   |-- widgets
   |   |   |-- __init__.py
   |   |   |-- barre_boutons.py
   |   |   |-- boutons
   |   |   |   |-- __init__.py
   |   |   |   |-- arreter.py
   |   |   |   |-- demarrer.py
   |   |   |   |-- pauser.py
   |   |   |   |-- reinitialiser.py
   |   |   |-- champs
   |   |   |   |-- nombre_personnes.py
   |   |   |   |-- temps_guerison.py
   |   |   |-- grille.py
   |   |   |-- parametres.py
   |   |   |-- sliders
   |   |   |   |-- __init__.py
   |   |   |   |-- taux_infectes.py
   |   |   |   |-- taux_letalite.py
   |   |   |   |-- taux_transmission.py
```


***
> Auteurs : Athène Rousseau-Rambach & Adrien Verstrepen