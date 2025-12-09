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