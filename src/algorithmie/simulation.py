from math import *
from random import uniform, randint
import pandas as pd
import random
import math
from .grille import Grille
from .personne import Personne

class Simulation :
    """
    On implémente ensuite la classe simulation, qui permet de construire toute la structure pour la simulation.
    """
    def __init__(self, maladie, largeur_fenetre, hauteur_fenetre, duree_cooldown_avant_naissance = 100, nb_personnes=50, taux_naissance=0.02):
        """
        Nb personnes est le nombre de personnes totales dans la simulation, tout état confondu.
        Maladie est l'objet de classe Maladie que la simulation va répandre.
        Liste personnes permet de stocker les personnes de la simulation.
        On stocke les statistiques qui peuvent servir pour la réalisation des statistiques dans l'attribut df_historique.
        On fait le stockage directement dans un dataframe pour que ce soit plus simple pour la réalisation des schémas matplotlib; car c'est la structure priviligiée pour ça.
        Iteration est le numéro de l'itération en cours.
        Grille est l'objet de classe Grille associé à la simulation.
        Taux naissance représente le pourcentage d'enfants nés dans la population.
        """
        self.nb_personnes = nb_personnes
        self.maladie = maladie
        self.liste_personnes = []
        self.df_historique = pd.DataFrame(columns=["nb_morts", "nb_total"])
        self.iterations = 0
        self.largeur_fenetre = largeur_fenetre
        self.hauteur_fenetre = hauteur_fenetre
        self.grille = Grille(taille_carreau=self.maladie.distance_infection, largeur_fenetre=largeur_fenetre, hauteur_fenetre=hauteur_fenetre)
        self.iterations_sans_infecte = 0
        self.duree_cooldown_avant_naissance = duree_cooldown_avant_naissance
        self.cooldown_avant_naissance = duree_cooldown_avant_naissance
        self.pourcentage_immunodeprimes = 0
        self.taux_naissance = taux_naissance

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
        for personne in self.liste_personnes:
            if randint(0, 100) <= pourcentage_infectes:
                personne.etre_infecte()
            if randint(0, 1000) <= 5:
                personne.etre_medecin()
        self.pourcentage_immunodeprimes = pourcentage_immunodeprimes
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
            voisins = [personne for personne in voisins if personne.etat == "sain"]
            for voisin in voisins :
                if voisin.cooldown_immunite <= 0 :
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
                personne.direction[0] += (centre_voisins[0] - personne.position[0]) * 0.0015
                personne.direction[1] += (centre_voisins[1] - personne.position[1]) * 0.0015
            if compteur_repulsion > 0:
                repulsion[0] /= compteur_repulsion
                repulsion[1] /= compteur_repulsion
                personne.direction[0] += repulsion[0] * 0.05
                personne.direction[1] += repulsion[1] * 0.05
            exploration = [random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05)]
            personne.direction[0] += exploration[0]
            personne.direction[1] += exploration[1]
            marge = 20
            force_mur = 1
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
            pas = 2
            x = personne.position[0] + personne.direction[0] * pas
            y = personne.position[1] + personne.direction[1] * pas
            x = min(max(0, x), self.grille.largeur)
            y = min(max(0, y), self.grille.hauteur)
            nouvelle_positions.append([x, y])
        for personne, position in zip(self.liste_personnes, nouvelle_positions):
            personne.se_deplace(position)
        self.grille.construire_grille(self.liste_personnes)
    
    def naissance(self, nb_nouvelles_personnes):
        for i in range(nb_nouvelles_personnes):
            position = [uniform(0, self.largeur_fenetre), uniform(0, self.hauteur_fenetre)]
            if randint(0, 100) < self.pourcentage_immunodeprimes:
                personne = Personne(etat="sain", immunodeprime="oui", position=position, id=i)
            else :
                personne = Personne(etat="sain", immunodeprime="non", position=position, id=i)
            if randint(0, 1000) <= 5:
                personne.etre_medecin()
            self.liste_personnes.append(personne)
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
        self.deplacement_boids_simplifie()
        self.propager_infection()
        if self.cooldown_avant_naissance >= 1 :
            self.cooldown_avant_naissance -= 1
        else :
            nb_total = self.df_historique.loc[self.iterations - 1].iloc[1] - self.df_historique.loc[self.iterations - 1].iloc[0]
            nb_naissance = math.ceil(nb_total * self.taux_naissance)
            self.naissance(nb_naissance)
            self.cooldown_avant_naissance = self.duree_cooldown_avant_naissance

        for personne in self.liste_personnes:
            if personne.etat == "infecte":
                voisins = self.grille.voisins_de_personne(personne)
                medecin_autour = 0
                for voisin in voisins:
                    if voisin.medecin == 1 and voisin.etat != "mort":
                        medecin_autour = 1

                risque_mort = self.maladie.taux_letalite / (2* self.maladie.temps_guerison)
                if personne.immunodeprime == "oui":
                    risque_mort *= 1.2
                if medecin_autour == 1 :
                    risque_mort /= 2
                if random.uniform(0, 100) <= risque_mort:
                    personne.mourir()
                    continue

                if medecin_autour == 1 :
                    personne.cpt_iterations_infection += 2
                else :
                    personne.cpt_iterations_infection += 1

                aleatoire = randint(0,5)
                if aleatoire == 0 :
                    personne.cpt_iterations_infection += 2
                elif aleatoire == 1 :
                    personne.cpt_iterations_infection += 1
                elif aleatoire == 2 :
                    personne.cpt_iterations_infection -= 1
                elif aleatoire == 3 :
                    personne.cpt_iterations_infection -= 2

                if self.maladie.temps_guerison != -1 and personne.cpt_iterations_infection >= self.maladie.temps_guerison:
                    if self.maladie.immunite_apres_guerison == True:
                        personne.etre_immunise()
                    else:
                        personne.guerir(self.maladie.temps_guerison)
                        personne.cpt_iterations_infection = 0
                    continue
            elif personne.etat == 'sain' :
                if personne.cooldown_immunite >= 1 :
                    personne.cooldown_immunite -= 1
            elif personne.etat == 'mort':
                if personne.cooldown_affichage_apres_mort >= 1 :
                    personne.cooldown_affichage_apres_mort -= 1
        if self.iterations_sans_infecte >= 200 :
            quantite_infectes_relance = 5
            for personne in self.liste_personnes:
                if random.uniform(0, 1000) <= quantite_infectes_relance and personne.etat != "mort":
                    personne.etre_infecte()
                    self.iterations_sans_infecte = 0
                    personne.cooldown_immunite = self.maladie.temps_guerison*0.75
        nb_morts = sum(1 for personne in self.liste_personnes if personne.etat == "mort")
        nb_infectes = sum(1 for personne in self.liste_personnes if personne.etat == "infecte")
        nb_total = len(self.liste_personnes)
        self.df_historique.loc[self.iterations] = [nb_morts, nb_total]
        if nb_infectes == 0 :
            self.iterations_sans_infecte += 1
        self.iterations += 1