from math import *
from random import uniform, sample, randint
import pandas as pd
import random
import math

class Personne :
    """
    On représente un individu de la simulation.

    Une personne possède un état de santé, une position en 2D, et différents attributs permettant de suivre son évolution.
    """
    def __init__(self, etat, immunodeprime, position, id=0, couleur="vert", medecin="non", cpt_iterations_infection=0):
        """
        La variable état représente l'état de santé de la personne, les valeurs possibles sont : "sain", "infecte", "immunise" et "mort".
        Par défaut, les personnes commencent avec un état sain et non malade.
        Le paramètre immunodéprimé peut valoir la valeur "oui" ou "non".
        La couleur correspond à l'état de la personne, on a choisi sain : vert, infecte : orange, mort : rouge et immunise : bleu.
        La valeur de medecin est 1 (oui) ou 0 (non).
        La position est représentée par une liste de deux éléments : l'abscisse x en premier et l'ordonnée y en deuxième, donnant donc [x,y].
        Nous avons choisi de faire une représentation en 2D.
        On met en place un système d'id pour pouvoir identifier chaque personne précisément.
        On compte aussi le nombre d'itérations depuis l'infection.
        """
        self.etat = etat
        self.immunodeprime = immunodeprime
        self.couleur = couleur
        self.medecin = medecin
        self.position = position
        self.id=id
        self.cpt_iterations_infection=cpt_iterations_infection

    def se_deplace(self, arrivee):
        """
        Se_déplace met à jour la nouvelle position d'une personne en vie.
        """
        if (self.etat != "mort"):
            self.position = arrivee
            
    def guerir(self):
        """
        Guerir sert à faire repasser une personne infectée à l'état sain si elle a survécu à la maladie.
        """
        self.etat = "sain"
        self.couleur = "vert"

    def mourir(self):
        """
        Mourir fait passer la personne à l'état mort.
        """
        self.etat = "mort"
        self.couleur = "rouge"

    def etre_infecte(self):
        """
        Etre infecté est appelée lors de l'infection d'une personne pour changer son état.
        """
        self.etat = "infecte"
        self.couleur = "orange"

    def etre_immunise(self):
        """
        La méthode etre immunise sera appelée si le fait de guérir d'une maladie rend la personne immunisée.
        """
        self.etat = "immunise"
        self.couleur = "bleu"

    def etre_medecin(self):
        """
        Etre médecin est appelée lors de l'initialisation pour affecter le rôle de médecin à une personne.
        """
        self.medecin = 1

    def etre_en_contact(self, position, distance_infection):
        """
        La méthode etre en contact permet de clalculer la distance entre deux points, dans notre cas c'est donc la position de deux personnes.
        """
        distance = sqrt((self.position[0]-position[0])**2 + (self.position[1]-position[1])**2)
        return True if distance <= distance_infection else False
    
    def __str__(self):
        """
        Dedans, la variable distance_infection correspond à la distance de propagation de la maladie.
        Si la distance entre les personnes est inférieure à la valeur à partir de laquelle une personne peut en contaminer une autre, on retourne True, sinon False, car la personne sera donc trop loin pour être contaminée.
        Finalement, __str__ affiche toutes les informations sur une personne.
        """
        return f"Personne n°{self.id} ; État : {self.etat} ; Immunodéprimé : {self.immunodeprime} ; Position : {self.position} ; Médecin : {self.medecin}\n"

class Maladie :
    """
    La classe Maladie est la classe contenant toutes les caractéristiques par rapport à la maladie qui va être simulée.
    Cette classe n'a pas de méthode car les données sont utilisées dans la classe Simulation, mais il n'y a pas de changement direct de la maladie lors de la simulation.
    """
    def __init__(self, taux_letalite, distance_infection, risque_transmission, immunite_apres_guerison, temps_guerison):
        """
        On ajoute en attribut le pourcentage de risque que quelqu'un infecté meurt de la maladie.
        La distance d'infection correspond à la distance maximale à partir de laquelle une personne peut en infecter une autre.
        Le risque transmission correspond au pourcentage de risque que quelqu'un d'infecté en infecte un autre qui serait assez proche pour être infecté.
        Sa valeur est donc un entier compris entre 1 et 100, avec 1% un risque très faible de transmission et 100% une transmission permanente.
        Immunité représente la possibilité d'être immunisé après avoir été infecté, les valeurs possibles sont donc "oui" et "non".
        Temps guérison représente le nombre d'itérations nécessaires pour être guéri, les valeurs possibles sont 5, 15, 25 et -1.
        5 représente une durée courte, 15 une durée moyenne, 25 une durée longue et -1 une durée infinie (on ne guéri jamais de la maladie).
        """
        self.taux_letalite = taux_letalite
        self.distance_infection = distance_infection
        self.risque_transmission = risque_transmission
        self.immunite_apres_guerison = immunite_apres_guerison
        self.temps_guerison = temps_guerison

class Grille:
    """
    On implémente une classe qui représente la grille qui nous permet d'optimiser la recherche des voisins d'une personne infectée.
    L'idée de cette classe est venue en remarquant que les recherches de voisins nécessitaient une comparaison avec toutes les autres personnes de la simulation, si l'implémentation était sans approche particulière.
    Cependant, cela prend énormément de temps, ce qui impacte la qualité et la fluidité de la simulation.
    Pour limiter cet effet, l'approche choisie est cette classe grille, qui partitionne la fenêtre en sous-fenêtres.
    L'intérêt est que la largeur d'un carreau de la grille est la même que la distance de propagation, ce qui assure qu'une personne infectéene peut infecter que des gens qui sont dans son carreau ou les 8 autres autour, mais pas plus loin.
    """
    def __init__(self, taille_carreau, largeur_fenetre, hauteur_fenetre):
        """
        Parmi les paramètres il y a la taille des carreaux, qui sont carrés, donc la longueur d'un côté correspond à la longeur de chacun de ses côtés.
        Il y a la largeur et la hauteur de la fenêtre, donc ses dimensions.
        On calcule le nombre de colonnes et de lignes pour la matrice en fonction des dimensions de la fenêtre et de la taille des carreaux.
        On stocke dans carreaux la liste des personnes présentes dedans.
        """
        self.taille_carreau = float(taille_carreau)
        self.largeur = largeur_fenetre
        self.hauteur = hauteur_fenetre
        self.nb_colonnes = int(self.largeur // self.taille_carreau) + 1
        self.nb_lignes = int(self.hauteur // self.taille_carreau) + 1
        self.carreaux = []
        for col in range(self.nb_colonnes):
            ligne = []
            for lig in range(self.nb_lignes):
                ligne.append([])
            self.carreaux.append(ligne)

    def coordonnees_carreau(self, position):
        """
        Cette méthode récupère les coordonnées du carreau dans la grille dans lequel se trouve une personne.
        """
        carreau_x = int(position[0] // self.taille_carreau)
        carreau_y = int(position[1] // self.taille_carreau)
        return carreau_x, carreau_y

    def construire_grille(self, personnes):
        """
        Cette méthode construit la grille à partir d'une liste de personnes.
        Comme cette fonction est appelée après la mise à jour des positions des personnes dans la fenêtre, on commence par vider toutes les cases avant de pouvoir remplir.
        On place chaque personne dans la bonne case.
        """
        for colonne in self.carreaux:
            for carreau in colonne:
                carreau.clear()
        for personne in personnes:
            carreau_x, carreau_y = self.coordonnees_carreau(personne.position)
            self.carreaux[carreau_x][carreau_y].append(personne)

    def voisins_de_personne(self, personne):
        """
        On récupère les voisins d'une personne dans son carreau ou les 8 autour.
        Ça permet de récupérer les personnes qui seront potentiellement infectées par la personne elle-même infectée.
        On commence déjà par récupérer le carreau auquel appartient la personne infectée.
        On pense bien à vérifier qu'on reste dans la grille.
        Par exemple, si on est dans le carreau tout en haut à droite, il faut bien penser à ne pas sortir de la grille.
        """
        carreau_x, carreau_y = self.coordonnees_carreau(personne.position)
        voisins = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                nouveau_carreau_x, nouveau_carreau_y = carreau_x + x, carreau_y + y
                if 0 <= nouveau_carreau_x < self.nb_colonnes and 0 <= nouveau_carreau_y < self.nb_lignes:
                    voisins.extend(self.carreaux[nouveau_carreau_x][nouveau_carreau_y])
        return voisins

class Simulation :
    """
    On implémente ensuite la classe simulation, qui permet de construire toute la structure pour la simulation.
    """
    def __init__(self, maladie, largeur_fenetre, hauteur_fenetre, nb_personnes=50):
        """
        Nb personnes est le nombre de personnes totales dans la simulation, tout état confondu.
        Maladie est l'objet de classe Maladie que la simulation va répandre.
        Liste personnes permet de stocker les personnes de la simulation.
        On stocke les statistiques qui peuvent servir pour la réalisation des statistiques dans l'attribut df_historique.
        On fait le stockage directement dans un dataframe pour que ce soit plus simple pour la réalisation des schémas matplotlib; car c'est la structure priviligiée pour ça.
        Iteration est le numéro de l'itération en cours.
        Grille est l'objet de classe Grille associé à la simulation.
        """
        self.nb_personnes = nb_personnes
        self.maladie = maladie
        self.liste_personnes = []
        self.df_historique = pd.DataFrame(columns=["nb_sains", "nb_infectes", "nb_immunises", "nb_morts", "nb_total"])
        self.iterations = 0
        self.grille = Grille(taille_carreau=self.maladie.distance_infection, largeur_fenetre=largeur_fenetre, hauteur_fenetre=hauteur_fenetre)

    def initialiser_population(self, largeur_fenetre, hauteur_fenetre, pourcentage_infectes = 5, pourcentage_immunodeprimes = 5):
        """
        On crée les personnes de la simulation et on infecte un échantillon.
        Par défaut, on met le pourcentage de personnes infectées à 5% mais l'utilisateur peut règler cette valeur.
        Il y a également un indicateur du pourcentage que représentent les personnes immunodéprimées parmi la population.
        On va initialiser chaque personne à une position aléatoire dans la fenêtre.
        On utilise randint pour tirer aléatoirement les chances qu'une personne soit immunodéprimée.
        Ensuite, on infecte le pourcentage de personnes infectées choisi par la personne.
        Pour cela, on tire aléatoirement le nombre de personnes qu'il faut.
        """
        for i in range(self.nb_personnes):
            position = [uniform(0, largeur_fenetre), uniform(0, hauteur_fenetre)]
            if randint(0, 100) < pourcentage_immunodeprimes:
                personne = Personne(etat="sain", immunodeprime="oui", position=position, id=i)
            else :
                personne = Personne(etat="sain", immunodeprime="non", position=position, id=i)
            self.liste_personnes.append(personne)
        nb_infectes_initiaux = int(self.nb_personnes * (pourcentage_infectes/100))
        infectes_initiaux = sample(self.liste_personnes, nb_infectes_initiaux)
        for personne in infectes_initiaux:
            personne.etre_infecte()
        nb_medecins = int(self.nb_personnes * 0.005)
        medecins = sample(self.liste_personnes, nb_medecins)
        for personne in medecins:
            personne.etre_medecin()
        self.grille.construire_grille(self.liste_personnes)
    
    def propager_infection(self):
        """
        On fait la propagation de la maladie aux personnes à côté d'une personne infectée.
        Pour chaque personne infectée, on récupère ses voisins, donc ceux dans sa case de la grille ou les 8 cas autour.
        On regarde si la distance entre les deux points est assez faible pour que la personne puisse être infectée.
        Comme la valeur de risque de transmission est un entier entre 1 et 100, on va récupérer une valeur aléatoire.
        Si elle est inférieure au pourcentage de risque de transmission, la personne est maintenant infectée.
        """
        infectes = [personne for personne in self.liste_personnes if personne.etat == "infecte"]
        for infecte in infectes:
            voisins = self.grille.voisins_de_personne(infecte)
            for voisin in voisins:
                if voisin.etat == "sain":
                    if infecte.etre_en_contact(voisin.position, self.maladie.distance_infection):
                        if randint(0, 100) < self.maladie.risque_transmission:
                            voisin.etre_infecte()
    
    def deplacements_aleatoires(self):
        """
        On fait se déplacer chaque personne de manière totalement aléatoire, pour ça on ajoute une petite variation en x et en y, dans un intervalle défini.
        On vérifie ensuite que la nouvelle position reste dans les limites de la fenêtre : si la personne dépasse le bord, on la replace exactement sur la limite.
        Finalement, on met à jour la position et on reconstruit la grille pour la prochaine itération.
        """
        random.seed()
        for personne in self.liste_personnes:
            x = personne.position[0] + random.randrange(-10, 10)
            y = personne.position[1] + random.randrange(-10, 10)
            if x < 0 :
                x = 0
            elif x > self.grille.largeur :
                x = self.grille.largeur
            if y < 0 :
                y = 0
            elif y > self.grille.hauteur :
                y = self.grille.hauteur
            personne.se_deplace([x, y])
        self.grille.construire_grille(self.liste_personnes)

    def deplacements_grille(self):
        """
        Chaque personne choisit un carreau voisin au hasard et se déplace si ce carreau est disponible
        À l'intérieur du carreau, la position est légèrement aléatoire pour éviter que tout le monde soit exactement au centre.
        """
        nouvelle_positions = []
        for personne in self.liste_personnes:
            carreau_x, carreau_y = self.grille.coordonnees_carreau(personne.position)
            direction_x = random.choice([-1, 0, 1])
            direction_y = random.choice([-1, 0, 1])
            nouveau_carreau_x = min(max(carreau_x + direction_x, 0), self.grille.nb_colonnes - 1)
            nouveau_carreau_y = min(max(carreau_y + direction_y, 0), self.grille.nb_lignes - 1)
            if self.grille.carreaux[nouveau_carreau_x][nouveau_carreau_y]:
                deplacement_x = random.uniform(-self.grille.taille_carreau/2, self.grille.taille_carreau/2)
                deplacement_y = random.uniform(-self.grille.taille_carreau/2, self.grille.taille_carreau/2)
            else:
                deplacement_x, deplacement_y = 0, 0
            x = min(max(nouveau_carreau_x * self.grille.taille_carreau + deplacement_x, 0), self.grille.largeur)
            y = min(max(nouveau_carreau_y * self.grille.taille_carreau + deplacement_y, 0), self.grille.hauteur)
            nouvelle_positions.append([x, y])
        for personne, position in zip(self.liste_personnes, nouvelle_positions):
            personne.se_deplace(position)
        self.grille.construire_grille(self.liste_personnes)
    
    def deplacement_stochastique_directionnel(self):
        """
        Chaque personne garde une direction générale qui change un peu entre chaque itération avec du hasard
        S'il y a des clusters fort proche de la personne, on limite l'attractivité de la direction, pour éviter des regroupements trop massifs.
        Cela permet d'avoir de la cohésion mais garder quand même des directions qui sont influencées par les voisins sans centrer tout le monde en un point.
        """
        nouvelle_positions = []
        for personne in self.liste_personnes:
            if not hasattr(personne, "direction"):
                angle = random.uniform(0, 2 * math.pi)
                personne.direction = [math.cos(angle), math.sin(angle)]
            densite = len(self.grille.voisins_de_personne(personne))
            exploration = [random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)]
            personne.direction[0] = 0.7 * personne.direction[0] + 0.3 * exploration[0] - 0.01 * densite
            personne.direction[1] = 0.7 * personne.direction[1] + 0.3 * exploration[1] - 0.01 * densite
            norme = math.sqrt(personne.direction[0]**2 + personne.direction[1]**2)
            personne.direction[0] /= norme
            personne.direction[1] /= norme
            pas = 10
            x = personne.position[0] + personne.direction[0] * pas
            y = personne.position[1] + personne.direction[1] * pas
            x = min(max(0, x), self.grille.largeur)
            y = min(max(0, y), self.grille.hauteur)
            nouvelle_positions.append([x, y])
        for personne, position in zip(self.liste_personnes, nouvelle_positions):
            personne.se_deplace(position)
        self.grille.construire_grille(self.liste_personnes)
 
    def deplacement_boids_simplifie(self):
        """ 
        Cette méthode met à jour la direction des personnes en utilisant deux des trois principes de Boids.
        D'abord, on calcule un point moyen des voisins proches pour ajuster légèrement la direction vers ce point.
        Ensuite, on ajoute une force de répulsion si des voisins sont trop proches pour éviter qu'ils se stackent.
        On ajoute aussi une petite valeur aléatoire pour modifier légèrement la direction à chaque étape.
        Enfin, on applique un poids aux murs pour qu'ils qui poussent les personnes vers l'intérieur lorsqu'elles s'approchent trop pour éviter les regroupement contre les murs.
        """
        nouvelle_positions = []
        for personne in self.liste_personnes :
            if not hasattr(personne, "direction"):
                angle = random.uniform(0, 2 * math.pi)
                personne.direction = [math.cos(angle), math.sin(angle)]
            voisins = self.grille.voisins_de_personne(personne)
            centre_voisins = [0, 0]
            repulsion = [0, 0]
            compteur_centre = 0
            compteur_repulsion = 0
            for voisin in voisins:
                if voisin is personne or voisin.etat == "mort":
                    continue
                direction_x = voisin.position[0] - personne.position[0]
                direction_y = voisin.position[1] - personne.position[1]
                distance = math.sqrt(direction_x**2 + direction_y**2)
                if distance < 50:
                    centre_voisins[0] += voisin.position[0]
                    centre_voisins[1] += voisin.position[1]
                    compteur_centre += 1
                if distance < 15:
                    repulsion[0] -= (voisin.position[0] - personne.position[0])
                    repulsion[1] -= (voisin.position[1] - personne.position[1])
                    compteur_repulsion += 1
            if compteur_centre > 0:
                centre_voisins[0] /= compteur_centre
                centre_voisins[1] /= compteur_centre
                personne.direction[0] += (centre_voisins[0] - personne.position[0]) * 0.003
                personne.direction[1] += (centre_voisins[1] - personne.position[1]) * 0.003
            if compteur_repulsion > 0:
                repulsion[0] /= compteur_repulsion
                repulsion[1] /= compteur_repulsion
                personne.direction[0] += repulsion[0] * 0.05
                personne.direction[1] += repulsion[1] * 0.05
            exploration = [random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05)]
            personne.direction[0] += exploration[0]
            personne.direction[1] += exploration[1]
            marge = 20
            force_mur = 0.1
            if personne.position[0] < marge:
                personne.direction[0] += force_mur
            if personne.position[0] > self.grille.largeur - marge:
                personne.direction[0] -= force_mur
            if personne.position[1] < marge:
                personne.direction[1] += force_mur
            if personne.position[1] > self.grille.hauteur - marge:
                personne.direction[1] -= force_mur
            norme = math.sqrt(personne.direction[0]**2 + personne.direction[1]**2)
            personne.direction[0] /= norme
            personne.direction[1] /= norme
            pas = 10
            x = personne.position[0] + personne.direction[0] * pas
            y = personne.position[1] + personne.direction[1] * pas
            x = min(max(0, x), self.grille.largeur)
            y = min(max(0, y), self.grille.hauteur)
            nouvelle_positions.append([x, y])
        for personne, position in zip(self.liste_personnes, nouvelle_positions):
            personne.se_deplace(position)
        self.grille.construire_grille(self.liste_personnes)
    
    def mise_a_jour_iteration(self):
        """
        On met à jour après chaque itération.
        La mise à jour de la position des personnes suit l'approche de Boids simplifié..
        Ensuite, on reconstruit la grille avec les nouvelles positions, on propage l'infection et on met à jour les états pour chaque personne.
        Pour les calculs, on va estimer que les personnes immunodéprimées ont deux fois plus de chances de mourir.
        Si la personne n'a pas une maladie permanente et qu'elle a survécu à toutes les itérations nécessaires pour que la maladie passe, la personne est guérie.
        Si on est immunisé après la maladie, la personne gagne ce statut, sinon elle est juste saine à nouveau.
        Finalement, on enregistre les statistiques actuelles sous forme de dataframe en calculant le nombre de personnes par état.
        """
        #self.deplacements_aleatoires()
        #self.deplacements_grille()
        #self.deplacement_stochastique_directionnel()
        #self.deplacement_cohesion_separation()
        self.deplacement_boids_simplifie()
        self.propager_infection()
        for personne in self.liste_personnes:
            if personne.etat == "infecte":
                voisins = self.grille.voisins_de_personne(personne)
                medecin_autour = 0
                for voisin in voisins:
                    if voisin.medecin == 1 and voisin.etat != "mort":
                        medecin_autour = 1

                if personne.cpt_iterations_infection == 0:
                    risque = self.maladie.taux_letalite
                    if personne.immunodeprime == "oui":
                        risque *= 1.5
                    if medecin_autour == 1 :
                        risque /= 2
                    if randint(1, 100) <= risque:
                        personne.mourir()
                        continue

                if medecin_autour == 1 :
                    personne.cpt_iterations_infection += 2
                else :
                    personne.cpt_iterations_infection += 1

                if self.maladie.temps_guerison != -1 and personne.cpt_iterations_infection >= self.maladie.temps_guerison:
                    if self.maladie.immunite_apres_guerison == "oui":
                        personne.etre_immunise()
                    else:
                        personne.guerir()
                    continue
        nb_sains = sum(1 for personne in self.liste_personnes if personne.etat == "sain")
        nb_infectes = sum(1 for personne in self.liste_personnes if personne.etat == "infecte")
        nb_immunises = sum(1 for personne in self.liste_personnes if personne.etat == "immunise")
        nb_morts = sum(1 for personne in self.liste_personnes if personne.etat == "mort")
        nb_total = nb_sains + nb_infectes + nb_immunises + nb_morts
        self.df_historique.loc[self.iterations] = [nb_sains, nb_infectes, nb_immunises, nb_morts, nb_total]

        self.iterations += 1