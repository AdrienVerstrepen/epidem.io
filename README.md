# epidem.io

## Description du projet
Ce projet est un outil de simulation permettant de suivre la propagation d'une épidémie de manière paramétrique, de façon réaliste, dans une interface qui se veut simple et explicite.

Voici l'adresse du dépôt contenant le code source : https://github.com/AdrienVerstrepen/epidem.io

## Installation et lancement
### Exécutable
Des fichiers exécutables sont fournis pour les systèmes Linux et Windows.
Ils sont disponibles dans l'onglet "release" sur github, ou bien dans le dossier src/bin.
Ces fichiers sont des exécutables indépendants permettant l'exécution de l'application.

### Python
Pour lancer l'application avec python, il faut récupérer le code source :
```
git clone https://github.com/AdrienVerstrepen/epidem.io && cd epidem.io
```
Puis vous pouvez lancer le programme avec : 
```
python -m src.ihm
```

## Fonctionnalités
* Simulation de la propagation d'épidémie en fonction de différents paramètres :
   * Effectif de la population
   * Pourcentage de transmission de la maladie
   * Pourcentage de mortalité de la maladie
   * Pourcentage de personnes qui sont initialement immunodéprimées
   * Pourcentage de patients 0 au lancement de la simulation
   * Durée d'infection de la maladie
   * Immunité lors de la guérison
* Suivi de la propagation :
   * Vous pouvez suivre l'évolution du nombre de personnes mortes au cours de la simulation dans l'onglet statistiques

## Organisation du projet

Voici le diagramme de Gantt, illustrant la répartition des tâches, dans le temps et par personne du projet :

### Structure du projet

À la racine du projet, vous retrouverez : 
* ce fichier
* deux dossiers dont voici une courte descriptions

Le dossier doc contient les différents documents liés à la documentation du projet : 
* Cahier des charges
* Documentation
* Diagramme de classe
* Diagramme de Gantt

Le dossier src contient le code source du projet :
* Package view
* Package algorithmie
* Exécutables
* Image(s)
* Tests

***
> Auteurs : Athène Rousseau-Rambach & Adrien Verstrepen