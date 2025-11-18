from classes import Personne
from ptest import TestCase

class TestPersonne(TestCase):
    def test_initialisation(self):
        p = Personne("sain", "non", [0, 0])
        self.assert_equals(p.etat, "sain")
        self.assert_equals(p.immunodeprime, "non")
        self.assert_equals(p.position, [0, 0])

    def test_mourir(self):
        p = Personne("sain", "non", [0, 0])
        p.mourir()
        self.assert_equals(p.etat, "mort")
        self.assert_equals(p.couleur, "rouge")

    def test_etre_infecte(self):
        p = Personne("sain", "non", [0, 0])
        p.etre_infecte()
        self.assert_equals(p.etat, "infecte")
        self.assert_equals(p.couleur, "orange")

    def test_deplacement(self):
        p = Personne("sain", "non", [1, 1])
        p.se_deplace([5, 5])
        self.assert_equals(p.position, [5, 5])

    def test_deplacement_mort(self):
        p = Personne("mort", "non", [1, 1])
        p.se_deplace([5, 5])
        self.assert_equals(p.position, [1, 1])

    def test_etre_en_contact(self):
        p = Personne("sain", "non", [0, 0])
        self.assert_true(p.etre_en_contact([1, 1], 2))
        self.assert_false(p.etre_en_contact([10, 10], 2))