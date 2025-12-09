from math import *

class Personne :
    """
    On représente un individu de la simulation.
    Une personne possède un état de santé, une position en 2D, et différents attributs permettant de suivre son évolution.
    """
    def __init__(self, etat, immunodeprime, position, id=0, couleur="vert", medecin=0, cpt_iterations_infection=0):
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
        La valeur cooldown immunite permet de donner un délai à chaque personne après qu'elle ait été guérie où elle ne peut pas être infectée par la maladie.
        """
        self.etat = etat
        self.immunodeprime = immunodeprime
        self.couleur = couleur
        self.medecin = medecin
        self.position = position
        self.id=id
        self.cpt_iterations_infection=cpt_iterations_infection
        self.cooldown_immunite = 0

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
        self.cooldown_immunite = 20

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