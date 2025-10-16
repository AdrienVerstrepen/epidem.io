import pandas as pd
from random import uniform
from classes import Simulation, Grille, Personne, Maladie
import time

def main():
    # c'est à adapter par la suite
    largeur_fenetre = 800
    hauteur_fenetre = 600

    maladie = Maladie(
        # le taux de létalité est un pourcentage, donc la valeur attfin_tempsue est entre 0 et 100
        taux_letalite=5,
        # les valeurs possibles sont entre 1 et 4, 1 étant très proche et 4 très éloigné
        # par soucis de facilité, je propose qu'on fasse cette distinction directement dans l'interface dans l'envoi des données
        # ça me permet d'utiliser ici direct des distances en fonction de la taille des fenetres
        distance_infection=2,
        # c'est également un pourcentage qui attfin_temps une valeur entre 1 et 100
        risque_transmission=30,
        immunite_apres_guerison="oui",
        # l'unité ici est le nombre d'itérations nécessaires pour guérir
        temps_guerison=10
    )
    simulation = Simulation(maladie, nb_personnes=10000)
    simulation.initialiser_population(pourcentage_infectes=2, pourcentage_immunodeprimes=10)

    # on enregistre l'état initial
    nb_sains = sum(1 for p in simulation.liste_personnes if p.etat == "sain")
    nb_infectes = sum(1 for p in simulation.liste_personnes if p.etat == "infecte")
    nb_immunises = sum(1 for p in simulation.liste_personnes if p.etat == "immunise")
    nb_morts = sum(1 for p in simulation.liste_personnes if p.etat == "mort")
    nb_total = nb_sains + nb_infectes + nb_immunises + nb_morts
    simulation.df_historique.loc[simulation.iterations] = [nb_sains, nb_infectes, nb_immunises, nb_morts, nb_total]
    simulation.iterations += 1
    
    nb_iterations = 20
    for i in range(nb_iterations):
        debut_temps = time.time()
        simulation.mise_a_jour_iteration()
        fin_temps = time.time()
        print(f"{i} :", fin_temps-debut_temps)

    print(simulation.df_historique)

if __name__ == "__main__":
    main()