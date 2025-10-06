from math import *
from random import uniform, sample, randint
import pandas as pd

# comme on utilise plus tard les positions, on met des variables globales ici pour pouvoir règler au fur et à mesure du développement
largeur_fenetre = 100
hauteur_fenetre = 100

# on commence par implémenter la classe personne, qui permet de construire chacun des individues de la simulation
class Personne :
    # par défaut, les personnes commencent saines (par rapport à cette maladie)
    # nous allons mettre le paramètre "médecin" à 0 pour le début, la mise en place des médecins sera faite plus tard
    def __init__(self, etat, immunodeprime, position, id=0, couleur="vert", medecin="non", cpt_iterations_infection=0):
        # l'état représente l'état de santé de la personne
        # les valeurs possibles sont : sain, infecte, immunise et mort
        self.etat = etat
        # le paramètre immunodéprimé peut valoir la valeur "oui" ou "non"
        self.immunodeprime = immunodeprime
        # la couleur correspond à l'état de la personne
        # sain : vert, infecte : orange, mort : rouge, immunise : bleu
        self.couleur = couleur
        # la valeur de medecin est "oui" ou "non"
        self.medecin = medecin
        # la position est représentée par une liste de deux éléments, on a l'abscisse x en premier et l'ordonnée y en deuxième, faisant donc [x,y]
        self.position = position
        # on met en place un système d'id pour pouvoir identifier chaque personne précisément
        self.id=id
        # on compte aussi le nombre d'itérations depuis l'infection
        self.cpt_iterations_infection=cpt_iterations_infection

    def se_deplace(self, arrivee):
        self.position = arrivee
            
    def guerir(self):
        self.etat = "sain"
        self.couleur = "vert"

    def mourir(self):
        self.etat = "mort"
        self.couleur = "rouge"

    def etre_infecte(self):
        self.etat = "infecte"
        self.couleur = "orange"

    def etre_immunise(self):
        self.etat = "immunise"
        self.couleur = "bleu"

    # cette méthode permet de clalculer la distance entre les deux points
    # la valeur position représente la position en x et y d'un autre point, et distance_infection correspond à la distance de propagation de la maladie
    def etre_en_contact(self, position, distance_infection):
        # si la distance entre les personnes est inférieure à la valeur à partir de laquelle une personne peut en contaminer une autre, on retourne True, sinon False
        distance = sqrt((self.position[0]-position[0])**2 + (self.position[1]-position[1])**2)
        return True if distance <= distance_infection else False


# on implémente maintenant la classe Maladie, qui est la classe contenant toutes les caractèristiques par rapport à la maladie qui va être simulée
class Maladie :
    def __init__(self, taux_letalite, distance_infection, risque_transmission, immunite_apres_guerison, temps_guerison):
        # on met en place le pourcentage de risque que quelqu'un infecté meurt de la maladie
        self.taux_letalite = taux_letalite
        # la distance d'infection correspond à la distance maximale à partir de laquelle une personne peut en infecter une autre
        # les valeurs possibles de distance sont de 1 à 4, 1 étant très proche et 4 très éloigné
        self.distance_infection = distance_infection
        # risque transmission correspond au pourcentage de risque que quelqu'un d'infecté en infecte un autre qui serait assez proche pour être infecté
        # sa valeur est donc un entier compris entre 1 et 100, avec 1% un risque très faible de transmission et 100% une transmission permanente
        self.risque_transmission = risque_transmission
        # immunité représente la possibilité d'avoir une immunité après avoir été infecté, les valeurs possibles sont donc "oui" et "non"
        self.immunite_apres_guerison = immunite_apres_guerison
        # cela représente le nombre d'itérations nécessaires pour être guéri
        # les valeurs possibles sont 5, 15, 25 et -1
        # 5 représente une durée courte, 15 une durée moyenne, 25 une durée longue et -1 une durée infinie (on en guéri jamais)
        self.temps_guerison = temps_guerison


# on implémente une classe qui représente la grille qui nous permet d'optimiser la recherche des voisins d'une personne infectée
class Grille:
    # on va prendre la distance de contamination comme taille de carreau, ça permet d'optimiser la taille des carreaux en fonction de l'utilisation qu'on en aura
    def __init__(self, taille_cellule, largeur_fenetre, hauteur_fenetre):
        self.taille_cellule = float(taille_cellule)
        self.largeur = largeur_fenetre
        self.hauteur = hauteur_fenetre
        # on calcule le nombre de colonnes et de lignes pour la matrice
        self.nb_colonnes = int(self.largeur // self.taille_cellule) + 1
        self.nb_lignes = int(self.hauteur // self.taille_cellule) + 1
        # on fait la matrice 2D avec listes vides
        # on stockera dans chaque case les personnes présentes grâce à une liste
        self.carreaux = []
        for col in range(self.nb_colonnes):
            ligne = []
            for lig in range(self.nb_lignes):
                ligne.append([])
            self.carreaux.append(ligne)

    # on récupère les coordonnées du carreau dans la grille dans lequel se trouve une personne
    def coordonnees_carreau(self, position):
        carreau_x = int(position[0] // self.taille_cellule)
        carreau_y = int(position[1] // self.taille_cellule)
        return carreau_x, carreau_y

    # on construit la grille à partir d'une liste de personnes
    def construire_grille(self, personnes):
        # on commence par vider toutes les cases avant de pouvoir remplir
        for colonne in self.carreaux:
            for carreau in colonne:
                carreau.clear()
        # on place chaque personne dans la bonne case
        for personne in personnes:
            carreau_x, carreau_y = self.coordonnees_carreau(personne.position)
            self.carreaux[carreau_x][carreau_y].append(personne)

    # on récupère les voisins d'une personne dans son carreau ou les 8 autour
    # ça permet de récupérer les personnes qui seront potentiellement infectées par la personne elle-même infectée
    def voisins_de_personne(self, personne):
        # on commence déjà par récupérer le carreau auquel appartient la personne infectée
        carreau_x, carreau_y = self.coordonnees_carreau(personne.position)
        voisins = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                nouveau_carreau_x, nouveau_carreau_y = carreau_x + x, carreau_y + y
                # on pense bien à vérifier qu'on reste dans la grille
                # par exemple si on est dans le carreau tout en haut à droite, il faut bien penser à ne pas sortir de la grille
                if 0 <= nouveau_carreau_x < self.nb_colonnes and 0 <= nouveau_carreau_y < self.nb_lignes:
                    voisins.extend(self.carreaux[nouveau_carreau_x][nouveau_carreau_y])
        return voisins
    

# on implémente ensuite la classe simulation, qui permet de construire toute la structure pour la simulation
class Simulation :
    def __init__(self, maladie, nb_personnes=50):
        # on garde le nombre de personnes totales dans la simulation
        self.nb_personnes = nb_personnes
        # on récupère les critères de la maladie entrés par l'utilisateur
        self.maladie = maladie
        # on stocke les personnes présentes
        self.liste_personnes = []
        # on stocke les statistiques qui peuvent servir pour la réalisation des statistiques
        # on fait directement en dataframe pour que ce soit plus simple pour la réalisation des schémas matplotlib
        self.df_historique = pd.DataFrame(columns=["nb_sains", "nb_infectes", "nb_immunises", "nb_morts", "nb_total"])
        # on garde aussi le nombre d'itérations
        self.iterations = 0
        # on crée la grille
        self.grille = Grille(taille_cellule=self.maladie.distance_infection, largeur_fenetre=largeur_fenetre, hauteur_fenetre=hauteur_fenetre)

    # on crée les personnes de la simulation et on infecte un échantillon
    # par défaut on met le pourcentage de personnes infectées à 5% mais l'utilisateur peut règler cette valeur
    # il y a également un indicateur des personnes immunodéprimées parmi la population
    def initialiser_population(self, pourcentage_infectes = 0.05, pourcentage_immunodeprimes = 0.05):
        # on crée le nombre de personnes que l'utilisateur veut
        for i in range(self.nb_personnes):
            # on va donner à chaque personne une position aléatoire dans la fenêtre
            # l'avantage d'uniform est que les valeurs ne sont pas forcément rondes, donc la répartitions sera plus aléatoire
            position = [uniform(0, largeur_fenetre), uniform(0, hauteur_fenetre)]
            # on crée la personne saine et on lui donne par défaut l'état sain
            personne = Personne(etat="sain", immunodeprime="non", position=position, id=i)
            # on ajoute la personen crée à la liste de toutes les personnes
            self.liste_personnes.append(personne)
        # on infecte le poucentage de personnes infectées choisi par la personne
        nb_infectes_initiaux = int(self.nb_personnes * pourcentage_infectes)
        # on tire aléatoirement le nombre de personnes qu'il faut
        infectes_initiaux = sample(self.liste_personnes, nb_infectes_initiaux)
        for personne in infectes_initiaux:
            personne.etre_infecte()
        # on pense bien à initialiser la grille avec les personnes générées
        self.grille.construire_grille(self.liste_personnes)
    
    # on fait la propagation de la maladie aux personnes à côté d'une personne infectée
    def propager_infection(self):
        # on commence par récupérer les personnes infectées
        infectes = [personne for personne in self.liste_personnes if personne.etat == "infecte"]
        for infecte in infectes:
            # on récupère ses voisins, donc ceux dans sa case ou les 8 cas autour
            voisins = self.grille.voisins_de_personne(infecte)
            for voisin in voisins:
                # on a pas besoin de regarder ceux qui sont déjà infectés, morts ou immunisés
                if voisin.etat == "sain":
                    # on regarde si la distance entre les deux points est assez faible pour que la personne puisse être infectée
                    if infecte.etre_en_contact(voisin.position, self.maladie.distance_infection):
                        # comme la valeur de risque de transmission est un entier entre 1 et 100, on va récupérer une valeur aléatoire
                        # si elle est inférieure au pourcentage de risque de transmission, la personne est maintenant infectée
                        if randint(0, 100) < self.maladie.risque_transmission:
                            voisin.etre_infecte()
    
    # on met à jour après chaque itération
    def mise_a_jour_iteration(self):
        # on ajoutera ici les mouvements

        # on reconstruit la grille avec les nouvelles positions
        self.grille.construire_grille(self.liste_personnes)
        # on propage l’infection
        self.propager_infection()
        # on met à jour les états pour chaque personne
        for personne in self.liste_personnes:
            if personne.etat == "infecte":
                personne.cpt_iterations_infection += 1
                # on teste si la personne va mourir
                # on va estimer que les personnes immunodéprimées ont deux fois plus de chances de mourir
                risque = self.maladie.taux_letalite
                if personne.immunodeprime == "oui":
                    risque *= 2
                if randint(1, 100) <= risque:
                    personne.mourir()
                # si la personne n'a pas une maladie permanente et qu'elle a survécu à toutes les itérations nécessaires pour que la maladie passe, la personne est guérie
                elif self.maladie.temps_guerison != -1 and personne.cpt_iterations_infection >= self.maladie.temps_guerison:
                    # si on est immunisé après la maladie, la personne gagne ce statut, sinon elle est juste saine à nouveau
                    if self.maladie.immunite_apres_guerison == "oui":
                        personne.etre_immunise()
                    else:
                        personne.guerir()
        # on enregistre les statistiques actuelles sous forme de dataframe 
        # pour ça, on calcule le nombre de personnes par état
        nb_sains = sum(1 for personne in self.liste_personnes if personne.etat == "sain")
        nb_infectes = sum(1 for personne in self.liste_personnes if personne.etat == "infecte")
        nb_immunises = sum(1 for personne in self.liste_personnes if personne.etat == "immunise")
        nb_morts = sum(1 for personne in self.liste_personnes if personne.etat == "mort")
        nb_total = nb_sains + nb_infectes + nb_immunises + nb_morts
        self.df_historique.loc[self.iterations] = [nb_sains, nb_infectes, nb_immunises, nb_morts, nb_total]

        # on augmente le compteur d’itérations
        self.iterations += 1
