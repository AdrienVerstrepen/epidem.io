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