from src.algorithmie.maladie import Maladie
from src.algorithmie.personne import Personne
from src.algorithmie.grille import Grille
from src.algorithmie.simulation import Simulation
from math import sqrt
import random
import math

# coverage run -m pytest
# coverage report -m

class TestMaladie:
    def test_initialisation(self):
        """
        On vérifie que l'objet Maladie stocke bien toutes les caractéristiques passées en argument.
        """
        maladie = Maladie(10, 5, 50, "oui", 15)

        assert maladie.taux_letalite == 10
        assert maladie.distance_infection == 5
        assert maladie.risque_transmission == 50
        assert maladie.immunite_apres_guerison == "oui"
        assert maladie.temps_guerison == 15

    def test_risque_transmission(self):
        """
        On vérifie que le risque de transmission reste dans un intervalle logique entre 1 et 100 pour représenter un pourcentage valide.
        """
        maladie = Maladie(5, 2, 100, "non", 5)

        assert 1 <= maladie.risque_transmission <= 100

    def test_temps_guerison(self):
        """
        On teste différentes valeurs de temps de guérison, y compris le cas -1.
        """
        for temps_guerison in [5, 15, 25, -1]:
            maladie = Maladie(5, 2, 50, "oui", temps_guerison)
            assert maladie.temps_guerison == temps_guerison

    def test_immunite(self):
        """
        On vérifie la prise en compte du paramètre d'immunité pour savoir si le système autorise ou non une protection après la maladie.
        """
        for immunite in ["oui", "non"]:
            maladie = Maladie(5, 2, 50, immunite, 5)
            assert maladie.immunite_apres_guerison == immunite


class TestPersonne:
    def test_initialisation(self):
        """
        On initialise une personne avec des paramètres précis et on vérifie que tous les compteurs internes sont corrects.
        """
        personne = Personne(etat="sain", immunodeprime="non", position=[0,0], id=1, couleur="vert", medecin=0, cpt_iterations_infection=0)

        assert personne.etat == "sain"
        assert personne.immunodeprime == "non"
        assert personne.position == [0,0]
        assert personne.id == 1
        assert personne.couleur == "vert"
        assert personne.medecin == 0
        assert personne.cpt_iterations_infection == 0
        assert personne.cooldown_immunite == 0
        assert personne.cooldown_affichage_apres_mort == -1

    def test_se_deplace(self):
        """
        On teste le mécanisme de déplacement.
        """
        personne = Personne("sain", "non", [0,0])
        personne.se_deplace([5,5])
        assert personne.position == [5,5]
        personne.mourir()
        personne.se_deplace([10,10])
        assert personne.position == [5,5]

    def test_guerir_mourir_infecte_immunise(self):
        """
        On vérifie que chaque méthode change correctement l'état, la couleur et les délais liés.
        """
        personne = Personne("infecte", "non", [0,0])

        personne.guerir(cooldown_immunite=10)
        assert personne.etat == "sain"
        assert personne.couleur == "vert"
        assert personne.cooldown_immunite == 10

        personne.mourir()
        assert personne.etat == "mort"
        assert personne.couleur == "rouge"
        assert personne.cooldown_affichage_apres_mort == 150

        personne.etre_infecte()
        assert personne.etat == "infecte"
        assert personne.couleur == "orange"

        personne.etre_immunise()
        assert personne.etat == "immunise"
        assert personne.couleur == "bleu"

    def test_etre_medecin(self):
        """
        On vérifie que la méthode dédiée permet de transformer une personne en médecin.
        """
        personne = Personne("sain", "non", [0,0], medecin=0)
        personne.etre_medecin()

        assert personne.medecin == 1

    def test_etre_en_contact(self):
        """
        On teste la détection de proximité : la personne doit détecter si un point est dans son périmètre d'infection selon la distance passée en paramètre.
        """
        personne = Personne("sain", "non", [0,0])

        assert personne.etre_en_contact([3,4], 5) is True
        assert personne.etre_en_contact([10,10], 5) is False

    def test_str(self):
        """
        On vérifie que la représentation textuelle de la personne contient bien les informations principales.
        """
        personne = Personne("sain", "non", [1,2], id=42, medecin=1)
        personne_texte = str(personne)

        assert "Personne n°42" in personne_texte
        assert "État : sain" in personne_texte
        assert "Immunodéprimé : non" in personne_texte
        assert "Position : [1, 2]" in personne_texte
        assert "Médecin : 1" in personne_texte


class TestGrille:
    def test_initialisation(self):
        """
        On vérifie que la grille crée le bon nombre de colonnes et de lignes en fonction de la taille des carreaux et des dimensions de la fenêtre.
        """
        grille = Grille(taille_carreau=10, largeur_fenetre=50, hauteur_fenetre=30)

        assert grille.taille_carreau == 10
        assert grille.largeur == 50
        assert grille.hauteur == 30
        assert grille.nb_colonnes == 6
        assert grille.nb_lignes == 4
        for colonne in grille.carreaux:
            for carreau in colonne:
                assert carreau == []

    def test_coordonnees_carreau(self):
        """
        On teste la logique de conversion : une position (x, y) doit être correctement rattachée à l'indice (i, j) du bon carreau de la grille.
        """
        grille = Grille(taille_carreau=10, largeur_fenetre=50, hauteur_fenetre=30)

        assert grille.coordonnees_carreau([0,0]) == (0,0)
        assert grille.coordonnees_carreau([9,9]) == (0,0)
        assert grille.coordonnees_carreau([10,0]) == (1,0)
        assert grille.coordonnees_carreau([49,29]) == (4,2)
        assert grille.coordonnees_carreau([50,30]) == (5,3)

    def test_construire_grille(self):
        """
        On vérifie qu'après la construction de la grille, chaque personne se retrouve bien rangée dans la liste du carreau correspondant à sa position.
        """
        grille = Grille(taille_carreau=10, largeur_fenetre=50, hauteur_fenetre=30)
        personne_1 = Personne("sain", "non", [5,5], id=1)
        personne_2 = Personne("sain", "non", [15,5], id=2)
        personne_3 = Personne("sain", "non", [49,29], id=3)
        grille.construire_grille([personne_1, personne_2, personne_3])

        assert personne_1 in grille.carreaux[0][0]
        assert personne_2 in grille.carreaux[1][0]
        assert personne_3 in grille.carreaux[4][2]

    def test_voisins_de_personne(self):
        """
        On vérifie que la méthode renvoie bien les personnes situées dans le carreau de l'individu et les carreaux adjacents.
        """
        grille = Grille(taille_carreau=10, largeur_fenetre=50, hauteur_fenetre=30)
        personne_1 = Personne("sain", "non", [5,5], id=1)
        personne_2 = Personne("sain", "non", [15,5], id=2)
        personne_3 = Personne("sain", "non", [0,15], id=3)
        personne_4 = Personne("sain", "non", [49,29], id=4)
        grille.construire_grille([personne_1, personne_2, personne_3, personne_4])
        voisins = grille.voisins_de_personne(personne_1)

        assert personne_1 in voisins
        assert personne_2 in voisins
        assert personne_3 in voisins
        assert personne_4 not in voisins


class TestSimulation:
    def configuration_simulation(self):
        """
        On prépare un environnement de simulation standardisé pour faciliter les tests suivants.
        """
        maladie = Maladie(temps_guerison=5, distance_infection=5, risque_transmission=50, immunite_apres_guerison=True, taux_letalite=10)
        simulation = Simulation(maladie, largeur_fenetre=100, hauteur_fenetre=100, nb_personnes=10, taux_naissance=0.1)
        return simulation

    def test_initialisation(self):
        """
        On vérifie que l'objet Simulation est correctement paramétré à la création avec la maladie, les dimensions de la fenêtre et les structures de stockage.
        """
        maladie = Maladie(10, 5, 50, "oui", 15)
        simulation = Simulation(maladie, 100, 50, nb_personnes=20)

        assert simulation.nb_personnes == 20
        assert simulation.maladie is maladie
        assert simulation.iterations == 0
        assert len(simulation.liste_personnes) == 0
        assert simulation.df_historique.empty
        assert simulation.grille.taille_carreau == 5
        assert simulation.grille.largeur == 100
        assert simulation.grille.hauteur == 50

    def test_initialiser_population(self):
        """
        On s'assure que la population est créée avec le bon nombre de personnes et que les répartitions (infectés, immunodéprimés) sont cohérentes.
        """
        maladie = Maladie(10, 5, 50, "oui", 15)
        simulation = Simulation(maladie, 100, 100, nb_personnes=50)
        simulation.initialiser_population(100, 100, pourcentage_infectes=10, pourcentage_immunodeprimes=20)

        assert len(simulation.liste_personnes) == 50
        nb_infectes = sum(1 for personne in simulation.liste_personnes if personne.etat == "infecte")
        assert 0 <= nb_infectes <= 50
        nb_immunodeprimes = sum(1 for personne in simulation.liste_personnes if personne.immunodeprime == "oui")
        assert 0 <= nb_immunodeprimes <= 50
        assert simulation.grille.carreaux

    def test_propager_infection(self):
        """
        On vérifie que la maladie se transmet bien entre deux personnes lorsqu'elles sont à proximité.
        """
        maladie = Maladie(100, 50, 100, "non", 10)
        simulation = Simulation(maladie, 200, 200, nb_personnes=2)
        personne_1 = Personne("infecte", "non", [50, 50], 1)
        personne_2 = Personne("sain", "non", [55, 55], 2)
        simulation.liste_personnes = [personne_1, personne_2]
        simulation.grille.construire_grille(simulation.liste_personnes)
        simulation.propager_infection()

        assert personne_2.etat == "infecte"

    def test_deplacements_aleatoires(self):
        """
        On teste le mouvement aléatoire pour vérifier que les personnes changent de position en restant dans les limites de la grille.
        """
        random.seed(0)
        maladie = Maladie(0, 5, 0, "non", 1)
        simulation = Simulation(maladie, 100, 100, nb_personnes=5)
        simulation.initialiser_population(100, 100, pourcentage_infectes=0, pourcentage_immunodeprimes=0)
        positions_initiales = [personne.position.copy() for personne in simulation.liste_personnes]
        simulation.deplacements_aleatoires()

        for personne in simulation.liste_personnes:
            x, y = personne.position
            assert 0 <= x <= simulation.grille.largeur
            assert 0 <= y <= simulation.grille.hauteur
        positions_apres = [personne.position for personne in simulation.liste_personnes]
        assert any(p_ini != p_apr for p_ini, p_apr in zip(positions_initiales, positions_apres))

    def test_naissance(self):
        """
        On vérifie que la méthode naissance ajoute le nombre de personnes demandé à la population.
        """
        maladie = Maladie(0, 5, 0, "non", 1)
        simulation = Simulation(maladie, 100, 100, nb_personnes=2)
        simulation.initialiser_population(100, 100, pourcentage_infectes=0)
        nb_initial = len(simulation.liste_personnes)
        simulation.naissance(3)

        assert len(simulation.liste_personnes) == nb_initial + 3

    def test_mise_a_jour_iteration_enregistre_stats(self):
        """
        On vérifie que chaque itération incrémente le compteur de temps et enregistre les données dans l'historique de la simulation.
        """
        maladie = Maladie(0, 5, 0, "non", 1)
        simulation = Simulation(maladie, 100, 100, nb_personnes=1)
        personne = Personne("infecte", "non", [10, 10], 1)
        simulation.liste_personnes = [personne]
        simulation.grille.construire_grille(simulation.liste_personnes)
        simulation.mise_a_jour_iteration()

        assert simulation.iterations == 1
        assert len(simulation.df_historique) == 1
        assert simulation.df_historique.loc[0, "nb_total"] == 1

    def test_mise_a_jour_iteration_guérison_et_mort_complexe(self, monkeypatch):
        """
        On vérifie le comportement simultané de plusieurs personnes à des états différents lors d'une mise à jour.
        """
        simulation = self.configuration_simulation()
        personne_infecte = Personne("infecte", "oui", [10, 10], id=1)
        personne_infecte.cpt_iterations_infection = simulation.maladie.temps_guerison + 1
        personne_saine = Personne("sain", "non", [20, 20], id=2)
        personne_saine.cooldown_immunite = 2
        personne_morte = Personne("mort", "non", [30, 30], id=3)
        personne_morte.cooldown_affichage_apres_mort = 3
        simulation.liste_personnes = [personne_infecte, personne_saine, personne_morte]
        simulation.grille.construire_grille(simulation.liste_personnes)
        simulation.iterations = 1
        simulation.df_historique.loc[0] = [0, len(simulation.liste_personnes)]
        monkeypatch.setattr(random, "uniform", lambda a, b: 100.0) 
        monkeypatch.setattr(random, "randint", lambda a, b: 0)
        simulation.mise_a_jour_iteration()

        assert personne_infecte.etat == "immunise"
        assert personne_saine.cooldown_immunite == 1
        assert personne_morte.cooldown_affichage_apres_mort == 2

    def test_deplacement_boids_complet(self, monkeypatch):
        """
        On vérifie que l'algorithme des Boids génère des directions cohérentes pour les personnes en mouvement.
        """
        simulation = self.configuration_simulation()
        personne_1 = Personne("sain", "non", [50, 50], id=0)
        personne_2 = Personne("sain", "non", [52, 52], id=1)
        simulation.liste_personnes = [personne_1, personne_2]
        monkeypatch.setattr(random, "uniform", lambda a, b: 0.01)
        simulation.deplacement_boids_simplifie()

        for personne in simulation.liste_personnes:
            norme = (personne.direction[0]**2 + personne.direction[1]**2)**0.5
            assert 0.99 <= norme <= 1.01

    def test_variation_compteur_infection(self, monkeypatch):
        """
        On vérifie précisément le calcul de l'évolution du compteur d'infection en fonction de la simulation.
        """
        simulation = self.configuration_simulation()
        personne = Personne("infecte", "non", [50, 50], id=1)
        personne.cpt_iterations_infection = 10
        simulation.liste_personnes = [personne]
        simulation.df_historique.loc[0] = [0, 1]
        simulation.iterations = 1
        simulation.grille.construire_grille(simulation.liste_personnes)
        monkeypatch.setattr("src.algorithmie.simulation.uniform", lambda a, b: 100.0)
        monkeypatch.setattr("src.algorithmie.simulation.randint", lambda a, b: 3)
        simulation.mise_a_jour_iteration()

        assert personne.cpt_iterations_infection == 9
    
    def test_couverture_medecin(self, monkeypatch):
        """
        On fait un test spécifique pour couvrir la ligne d'attribution du rôle de médecin.
        """
        maladie = Maladie(10, 5, 50, "oui", 15)
        simulation = Simulation(maladie, 100, 100, nb_personnes=1)
        monkeypatch.setattr("src.algorithmie.simulation.randint", lambda a, b: 0)
        monkeypatch.setattr("src.algorithmie.simulation.uniform", lambda a, b: 50.0)
        simulation.initialiser_population(100, 100)

        assert simulation.liste_personnes[0].medecin == 1

    def test_deplacements_aleatoires_limites(self, monkeypatch):
        """
        On vérifie que les déplacements aléatoires respectent les limites de la grille.
        """
        maladie = Maladie(10, 5, 0, "non", 0)
        simulation = Simulation(maladie, 100, 100, nb_personnes=2)
        personne_1 = Personne("sain", "non", [2, 2], id=1)
        personne_2 = Personne("sain", "non", [98, 98], id=2)
        simulation.liste_personnes = [personne_1, personne_2]
        situation_random = iter([-10, -10, 10, 10])
        monkeypatch.setattr("random.randrange", lambda a, b: next(situation_random))
        simulation.deplacements_aleatoires()

        assert personne_1.position == [0, 0]
        assert personne_2.position == [100, 100]

    def test_deplacements_grille(self, monkeypatch):
        """
        On vérifie que le déplacement dans la grille déplace correctement les personnes vers les carreaux cibles.
        """
        maladie = Maladie(10, 5, 50, "non", 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=2)
        personne_1 = Personne("sain", "non", [2, 2], id=1)
        personne_2 = Personne("sain", "non", [85, 85], id=2)
        simulation.liste_personnes = [personne_1, personne_2]
        simulation.grille.construire_grille(simulation.liste_personnes)
        simulation.grille.carreaux[0][0] = []
        simulation.grille.carreaux[18][18] = [personne_2]
        cas_choix = iter([0, 0, 1, 1])
        monkeypatch.setattr("random.choice", lambda x: next(cas_choix))
        cas_uniforme = iter([2.5, 2.5])
        monkeypatch.setattr("random.uniform", lambda a, b: next(cas_uniforme))
        simulation.deplacements_grille()

        assert personne_1.position == [0.0, 0.0]
        assert personne_2.position == [92.5, 92.5]
    
    def test_deplacement_stochastique_directionnel_norme_nulle(self, monkeypatch):
        """
        On vérifie que le déplacement stochastique gère correctement le cas où la direction initiale d'une personne est nulle.
        """
        maladie = Maladie(10, 5, 50, "non", 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=1)
        personne_direction_nulle = Personne("sain", "non", [50, 50], id=1)
        personne_direction_nulle.direction = [0.0, 0.0]
        simulation.liste_personnes = [personne_direction_nulle]
        simulation.grille.construire_grille(simulation.liste_personnes)
        densite = len(simulation.grille.voisins_de_personne(personne_direction_nulle))
        compensation = (0.01 * densite) / 0.3
        valeurs_uniformes = iter([compensation, compensation, math.pi / 2])
        monkeypatch.setattr("random.uniform", lambda a, b: next(valeurs_uniformes))
        simulation.deplacement_stochastique_directionnel()

        assert math.isclose(personne_direction_nulle.direction[0], 0.0, abs_tol=1e-7)
        assert math.isclose(personne_direction_nulle.direction[1], 1.0, abs_tol=1e-7)

    def test_deplacement_stochastique_directionnel_complet(self, monkeypatch):
        """
        On vérifie que les déplacements directionnels mettent à jour les positions sans sortir des limites de la simulation.
        """
        maladie = Maladie(10, 5, 50, "non", 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=2)
        personne_1 = Personne("sain", "non", [50, 50], id=1)
        personne_2 = Personne("sain", "non", [0, 0], id=2)
        personne_1.direction = [1.0, 0.0]
        personne_2.direction = [-1.0, 0.0]
        simulation.liste_personnes = [personne_1, personne_2]
        simulation.grille.construire_grille(simulation.liste_personnes)
        valeurs_uniformes = iter([0.0, 0.0, 0.0, 0.0])
        monkeypatch.setattr("random.uniform", lambda a, b: next(valeurs_uniformes))
        simulation.deplacement_stochastique_directionnel()

        assert personne_2.position[0] == 0
        assert 0 <= personne_1.position[0] <= 100

    def test_deplacement_boids_simplifie_complet(self, monkeypatch):
        """
        On teste pour s'assurer qu'on ignore les morts et réagit aux obstacles murs de la fenêtre.
        """
        maladie = Maladie(10, 5, 50, "non", 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=3)
        personne_centrale = Personne("sain", "non", [10, 10], id=1)
        personne_proche = Personne("sain", "non", [12, 12], id=2)
        personne_morte = Personne("mort", "non", [11, 11], id=3)
        simulation.liste_personnes = [personne_centrale, personne_proche, personne_morte]
        simulation.grille.construire_grille(simulation.liste_personnes)
        valeurs_initiales = iter([0.0] * 20)
        monkeypatch.setattr("random.uniform", lambda a, b: next(valeurs_initiales))
        simulation.deplacement_boids_simplifie()

        assert hasattr(personne_centrale, "direction")
        
        personne_mur = Personne("sain", "non", [2, 2], id=4)
        personne_mur.direction = [-1.0, -1.0]
        simulation.liste_personnes = [personne_mur]
        simulation.grille.construire_grille(simulation.liste_personnes)
        valeurs_murs = iter([0.0] * 10)
        monkeypatch.setattr("random.uniform", lambda a, b: next(valeurs_murs))
        simulation.deplacement_boids_simplifie()

        assert personne_mur.direction[0] > -1.0
        assert personne_mur.direction[1] > -1.0

    def test_deplacement_boids_murs(self, monkeypatch):
        """
        On vérifie que les personnes sont repoussés par les quatre murs de la grille lorsqu'ils s'en approchent.
        """
        maladie = Maladie(10, 5, 50, "non", 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=4)
        personne_gauche = Personne("sain", "non", [5, 50], id=1)
        personne_droite = Personne("sain", "non", [95, 50], id=2)
        personne_haut = Personne("sain", "non", [50, 5], id=3)
        personne_bas = Personne("sain", "non", [50, 95], id=4)
        personnes = [personne_gauche, personne_droite, personne_haut, personne_bas]
        for personne in personnes:
            personne.direction = [0.0, 0.0]
        simulation.liste_personnes = personnes
        simulation.grille.construire_grille(simulation.liste_personnes)
        valeurs_exploration = iter([0.0] * 10)
        monkeypatch.setattr("random.uniform", lambda a, b: next(valeurs_exploration))
        simulation.deplacement_boids_simplifie()

        assert personne_gauche.direction[0] > 0
        assert personne_droite.direction[0] < 0
        assert personne_haut.direction[1] > 0
        assert personne_bas.direction[1] < 0

    def test_naissance_couverture_totale(self, monkeypatch):
        """
        On vérifie l'attribution correcte des rôles lors de la création de nouvelles personnes.
        """
        maladie = Maladie(10, 5, 50, "non", 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=0)
        simulation.pourcentage_immunodeprimes = 20
        valeurs_uniform = iter([10.0, 10.0, 20.0, 20.0, 30.0, 30.0])
        monkeypatch.setattr("src.algorithmie.simulation.uniform", lambda a, b: next(valeurs_uniform))
        valeurs_randint = iter([10, 0, 50, 100, 90, 6])
        monkeypatch.setattr("src.algorithmie.simulation.randint", lambda a, b: next(valeurs_randint))
        simulation.naissance(3)

        assert len(simulation.liste_personnes) == 3
        
        personne_1 = simulation.liste_personnes[0]
        assert personne_1.immunodeprime == "oui"
        assert personne_1.medecin == 1

        personne_2 = simulation.liste_personnes[1]
        assert personne_2.immunodeprime == "non"
        assert personne_2.medecin == 0

        personne_3 = simulation.liste_personnes[2]
        assert personne_3.immunodeprime == "non"
        assert personne_3.medecin == 0

    def test_mise_a_jour_naissances(self, monkeypatch):
        """
        On vérifie que la génération des naissances respecte le cooldown et qu'on ajoute le bon nombre de personnes à la population.
        """
        maladie = Maladie(10, 5, 50, True, 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=0)
        simulation.df_historique.loc[0] = [0, 10] 
        simulation.iterations = 1
        simulation.taux_naissance = 0.5
        simulation.liste_personnes = [Personne("sain", "non", [50, 50], id=i) for i in range(10)]
        monkeypatch.setattr("random.uniform", lambda a, b: 0.1)
        monkeypatch.setattr("src.algorithmie.simulation.uniform", lambda a, b: 10.0)
        monkeypatch.setattr("src.algorithmie.simulation.randint", lambda a, b: 50)

        simulation.cooldown_avant_naissance = 2
        simulation.mise_a_jour_iteration()
        assert simulation.cooldown_avant_naissance == 1

        simulation.cooldown_avant_naissance = 0
        simulation.duree_cooldown_avant_naissance = 5
        simulation.mise_a_jour_iteration()
        assert len(simulation.liste_personnes) == 15
        assert simulation.cooldown_avant_naissance == 5

    def test_mise_a_jour_survie_et_guerison(self, monkeypatch):
        """
        On vérifie que la présence d'un médecin réduit le risque de mort et accélère la guérison d'une personne infectée.
        """
        maladie = Maladie(100, 10, 50, True, 10) 
        simulation = Simulation(maladie, 100, 100, nb_personnes=0)
        personne_2 = Personne("infecte", "non", [50, 51], id=2)
        personne_2.cpt_iterations_infection = 0
        medecin = Personne("sain", "non", [50, 52], id=3)
        medecin.medecin = 1
        simulation.liste_personnes = [personne_2, medecin]
        simulation.df_historique.loc[0] = [0, 2]
        simulation.iterations = 1
        simulation.cooldown_avant_naissance = 10
        monkeypatch.setattr(simulation.grille, "voisins_de_personne", lambda personne: [medecin] if personne.id == 2 else [])
        def verification_uniforme(a, b):
            if a == 0 and b == 100:
                return 99.0
            return 0.5
        monkeypatch.setattr("random.uniform", verification_uniforme)
        monkeypatch.setattr("src.algorithmie.simulation.randint", lambda a, b: 0)
        monkeypatch.setattr(simulation, "propager_infection", lambda: None)
        simulation.mise_a_jour_iteration()
        
        assert personne_2.cpt_iterations_infection >= 4
        assert personne_2.etat == "infecte"

    def test_relance_epidemie(self, monkeypatch):
        """
        On vérifie que la simulation peut relancer l'épidémie si aucun infecté n'est présent après une longue période.
        """
        maladie = Maladie(10, 5, 50, True, 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=1)
        personne = Personne("sain", "non", [50, 50], id=1)
        simulation.liste_personnes = [personne]
        simulation.df_historique.loc[0] = [0, 1]
        simulation.iterations = 1
        simulation.iterations_sans_infecte = 200
        monkeypatch.setattr("random.uniform", lambda a, b: 1.0)
        simulation.mise_a_jour_iteration()
        
        assert personne.etat == "infecte"
        assert simulation.iterations_sans_infecte == 0
        assert personne.cooldown_immunite == maladie.temps_guerison * 0.75

    def test_mise_a_jour_complet_infectes(self, monkeypatch):
        """
        On valide le cycle de vie complet des infectés pendant une itération.
        """
        maladie = Maladie(50, 10, 50, False, 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=0)
        personne_morte = Personne("infecte", "non", [10, 10], id=1)
        personne_temoin = Personne("infecte", "non", [20, 20], id=2)
        personne_temoin.cpt_iterations_infection = 3
        personne_guerison = Personne("infecte", "non", [30, 30], id=3)
        personne_guerison.cpt_iterations_infection = 8
        simulation.liste_personnes = [personne_morte, personne_temoin, personne_guerison]
        simulation.df_historique.loc[0] = [0, 3]
        simulation.iterations = 1
        simulation.cooldown_avant_naissance = 10
        monkeypatch.setattr(simulation.grille, "voisins_de_personne", lambda p: [])
        monkeypatch.setattr(simulation, "deplacement_boids_simplifie", lambda: None)
        monkeypatch.setattr(simulation, "propager_infection", lambda: None)
        calcul_survie = iter([0.0, 99.0, 99.0])
        def verification_uniforme(a, b):
            if a == 0 and b == 100:
                return next(calcul_survie)
            return 0.5
        monkeypatch.setattr("random.uniform", verification_uniforme)
        monkeypatch.setattr("src.algorithmie.simulation.randint", lambda a, b: 1)
        simulation.mise_a_jour_iteration()

        assert personne_morte.etat == "mort"
        assert personne_morte.cooldown_affichage_apres_mort == 150

        assert personne_temoin.cpt_iterations_infection == 5
        assert personne_temoin.etat == "infecte"

        assert personne_guerison.etat == "sain"
        assert personne_guerison.cpt_iterations_infection == 0
        assert personne_guerison.cooldown_immunite == 10