from src.classes import Maladie, Personne, Grille, Simulation
from math import sqrt

# pour lancer le code, il faut se mettre au niveau d'epidem.io et entrer pytest src/tests/test_classes.py dans le terminal

class TestMaladie :
    def test_initialisation(self):
        maladie = Maladie(10, 5, 50, "oui", 15)
        assert maladie.taux_letalite == 10
        assert maladie.distance_infection == 5
        assert maladie.risque_transmission == 50
        assert maladie.immunite_apres_guerison == "oui"
        assert maladie.temps_guerison == 15

    def test_risque_transmission(self):
        maladie = Maladie(5, 2, 100, "non", 5)
        assert maladie.risque_transmission is not None
        assert 1 <= maladie.risque_transmission <= 100

    def test_temps_guerison(self):
        for temps_guerison in [5, 15, 25, -1]:
            maladie = Maladie(5, 2, 50, "oui", temps_guerison)
            assert temps_guerison in [5, 15, 25, -1]

    def test_immunite(self):
        for immunité in ["oui", "non"]:
            maladie = Maladie(5, 2, 50, immunité, 5)
            assert immunité in ["oui", "non"]

class TestPersonne :
    def test_initialisation(self):
        personne = Personne(etat="sain", immunodeprime="non", position=[0,0], id=1, couleur="vert", medecin="non", cpt_iterations_infection=0)
        assert personne.etat == "sain"
        assert personne.immunodeprime == "non"
        assert personne.position == [0,0]
        assert personne.id == 1
        assert personne.couleur == "vert"
        assert personne.medecin == "non"
        assert personne.cpt_iterations_infection == 0

    def test_se_deplace(self):
        personne = Personne("sain", "non", [0,0])
        personne.se_deplace([5,5])
        assert personne.position == [5,5]

        personne.mourir()
        personne.se_deplace([10,10])
        assert personne.position == [5,5]

    def test_guerir_mourir_infecte_immunise(self):
        personne = Personne("infecte", "non", [0,0])
        
        personne.guerir()
        assert personne.etat == "sain"
        assert personne.couleur == "vert"

        personne.mourir()
        assert personne.etat == "mort"
        assert personne.couleur == "rouge"

        personne.etre_infecte()
        assert personne.etat == "infecte"
        assert personne.couleur == "orange"

        personne.etre_immunise()
        assert personne.etat == "immunise"
        assert personne.couleur == "bleu"

    def test_etre_en_contact(self):
        personne = Personne("sain", "non", [0,0])
        assert personne.etre_en_contact([3,4], 5) is True
        assert personne.etre_en_contact([10,10], 5) is False

    def test_str(self):
        personne = Personne("sain", "non", [1,2], id=42, medecin="oui")
        s = str(personne)
        assert "Personne n°42" in s
        assert "État : sain" in s
        assert "Immunodéprimé : non" in s
        assert "Position : [1, 2]" in s
        assert "Médecin : oui" in s

class TestGrille:
    def test_initialisation(self):
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
        grille = Grille(taille_carreau=10, largeur_fenetre=50, hauteur_fenetre=30)
        assert grille.coordonnees_carreau([0,0]) == (0,0)
        assert grille.coordonnees_carreau([9,9]) == (0,0)
        assert grille.coordonnees_carreau([10,0]) == (1,0)
        assert grille.coordonnees_carreau([49,29]) == (4,2)

    def test_construire_grille(self):
        grille = Grille(taille_carreau=10, largeur_fenetre=50, hauteur_fenetre=30)
        personnes_1 = Personne("sain", "non", [5,5], id=1)
        personnes_2 = Personne("sain", "non", [15,5], id=2)
        personnes_3 = Personne("sain", "non", [49,29], id=3)

        grille.construire_grille([personnes_1,personnes_2,personnes_3])
        assert personnes_1 in grille.carreaux[0][0]
        assert personnes_2 in grille.carreaux[1][0]
        assert personnes_3 in grille.carreaux[4][2]

    def test_voisins_de_personne(self):
        grille = Grille(taille_carreau=10, largeur_fenetre=50, hauteur_fenetre=30)
        personnes_1 = Personne("sain", "non", [5,5], id=1)
        personnes_2 = Personne("sain", "non", [15,5], id=2)
        personnes_3 = Personne("sain", "non", [0,15], id=3)

        grille.construire_grille([personnes_1,personnes_2,personnes_3])
        voisins_p1 = grille.voisins_de_personne(personnes_1)
        assert personnes_1 in voisins_p1
        assert personnes_2 in voisins_p1
        assert personnes_3 in voisins_p1

class TestSimulation:
    def test_initialisation(self):
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
        maladie = Maladie(10, 5, 50, "oui", 15)
        simulation = Simulation(maladie, 100, 100, nb_personnes=50)
        simulation.initialiser_population(100, 100, pourcentage_infectes=10, pourcentage_immunodeprimes=20)

        assert len(simulation.liste_personnes) == 50
        nb_infectes = sum(1 for personne in simulation.liste_personnes if personne.etat == "infecte")
        assert nb_infectes == 5
        nb_immunodeprimes = sum(1 for personne in simulation.liste_personnes if personne.immunodeprime == "oui")
        assert 0 < nb_immunodeprimes <= 50
        assert simulation.grille.carreaux

    def test_propager_infection(self):
        maladie = Maladie(100, 50, 100, "non", 10)
        simulation = Simulation(maladie, 200, 200, nb_personnes=2)
        personne_1 = Personne("infecte", "non", [50, 50], 1)
        personne_2 = Personne("sain", "non", [55, 55], 2)

        simulation.liste_personnes = [personne_1, personne_2]
        simulation.grille.construire_grille(simulation.liste_personnes)
        simulation.propager_infection()
        assert personne_2.etat == "infecte"

    def test_deplacements_aleatoires(self):
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
        assert any(position_initiale != position_finale for position_initiale, position_finale in zip(positions_initiales, positions_apres))
        personnes_dans_grille = all(
            any(personne in carreau for colonne in simulation.grille.carreaux for carreau in colonne)
            for personne in simulation.liste_personnes
        )
        assert personnes_dans_grille
    
    def test_deplacements_grille(self):
        maladie = Maladie(0, 5, 0, "non", 1)
        simulation = Simulation(maladie, 50, 50, nb_personnes=5)
        simulation.initialiser_population(50, 50, pourcentage_infectes=0, pourcentage_immunodeprimes=0)
        positions_initiales = [personne.position.copy() for personne in simulation.liste_personnes]
        simulation.deplacements_grille()
        for personne in simulation.liste_personnes:
            x, y = personne.position
            assert 0 <= x <= simulation.grille.largeur
            assert 0 <= y <= simulation.grille.hauteur
        positions_apres = [personne.position for personne in simulation.liste_personnes]
        assert any(position_initiale != position_finale for position_initiale, position_finale in zip(positions_initiales, positions_apres))
        personnes_dans_grille = all(
            any(personne in carreau for colonne in simulation.grille.carreaux for carreau in colonne)
            for personne in simulation.liste_personnes
        )
        assert personnes_dans_grille
    
    def test_deplacement_stochastique_directionnel(self):
        maladie = Maladie(0, 5, 0, "non", 1)
        simulation = Simulation(maladie, 100, 100, nb_personnes=5)
        simulation.initialiser_population(100, 100, pourcentage_infectes=0, pourcentage_immunodeprimes=0)
        positions_initiales = [personne.position.copy() for personne in simulation.liste_personnes]
        simulation.deplacement_stochastique_directionnel()
        for personne in simulation.liste_personnes:
            x, y = personne.position
            assert 0 <= x <= simulation.grille.largeur
            assert 0 <= y <= simulation.grille.hauteur
        positions_apres = [personne.position for personne in simulation.liste_personnes]
        assert any(position_initiale != position_finale for position_initiale, position_finale in zip(positions_initiales, positions_apres))
        personnes_dans_grille = all(
            any(personne in carreau for colonne in simulation.grille.carreaux for carreau in colonne)
            for personne in simulation.liste_personnes
        )
        assert personnes_dans_grille


    def test_mise_a_jour_iteration_enregistre_stats(self):
        maladie = Maladie(0, 5, 0, "non", 1)
        simulation = Simulation(maladie, 100, 100, nb_personnes=1)
        personne = Personne("infecte", "non", [10, 10], 1)
        simulation.liste_personnes = [personne]
        simulation.grille.construire_grille(simulation.liste_personnes)

        simulation.mise_a_jour_iteration()
        assert simulation.iterations == 1
        assert len(simulation.df_historique) == 1
        assert simulation.df_historique.loc[0, "nb_total"] == 1

    def test_mise_a_jour_iteration_guerison(self):
        maladie = Maladie(0, 5, 0, "oui", 1)
        simulation = Simulation(maladie, 100, 100, nb_personnes=1)
        personne = Personne("infecte", "non", [10, 10], 1)
        simulation.liste_personnes = [personne]
        simulation.grille.construire_grille(simulation.liste_personnes)

        simulation.mise_a_jour_iteration()
        assert personne.etat == "immunise"

    def test_mise_a_jour_iteration_mort(self, monkeypatch):
        maladie = Maladie(100, 5, 0, "non", 10)
        simulation = Simulation(maladie, 100, 100, nb_personnes=1)
        personne = Personne("infecte", "non", [10, 10], 1)
        simulation.liste_personnes = [personne]
        simulation.grille.construire_grille(simulation.liste_personnes)

        monkeypatch.setattr("random.randint", lambda a, b: 1)
        simulation.mise_a_jour_iteration()
        assert personne.etat == "mort"