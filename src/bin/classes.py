from math import *
from random import uniform, sample, random

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
        self.liste_historique_iterations = []
        # on garde aussi le nombre d'itérations
        self.iterations = 0

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