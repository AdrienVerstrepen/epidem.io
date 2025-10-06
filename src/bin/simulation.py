from math import *

# on commence par implémenter la classe personne, qui permet de construire chacun des individues de la simulation
class Personne :
    # par défaut, les personnes commencent saines (par rapport à cette maladie)
    # nous allons mettre le paramètre "médecin" à 0 pour le début, la mise en place des médecins sera faite plus tard
    def __init__(self, etat, immunodeprime, position, couleur="vert", medecin="non"):
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
        # la valeur position représente la position en x et y d'un autre point, et le rayon correspond à la distance de propagation de la maladie
        def etre_en_contact(self, position, rayon):
            # si la distance entre les personnes est inférieure à la valeur à partir de laquelle une personne peut en contaminer une autre, on retourne 1, sinon 0
            distance = sqrt((self.position[0]-position[0])**2 + (self.position[1]-position[1])**2)
            return 1 if distance <= rayon else 0