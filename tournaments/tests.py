"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from tournaments.pairing import Pairing


class PairingTest(TestCase):
    def __init__(self, methodName='runTest'):
        TestCase.__init__(self, methodName=methodName)
        self.players = [
                        {'name': 'Alexandra Kosteniuk', 'rating': 2457, 'title': 8},
                        {'name': 'Alisa Galliamova', 'rating': 2484, 'title': 7},
                        {'name': 'Anna Muzychuk', 'rating': 2598, 'title': 8},
                        {'name': 'Antoaneta Stefanova', 'rating': 2518, 'title': 8},
                        {'name': 'Betul Cemre Yildiz', 'rating': 2333, 'title': 6},
                        {'name': 'Elina Danielian', 'rating': 2484, 'title': 8},
                        {'name': 'Hou Yifan', 'rating': 2623, 'title': 8},
                        {'name': 'Humpy Koneru', 'rating': 2589, 'title': 8},
                        {'name': 'Kateryna Lahno', 'rating': 2546, 'title': 8},
                        {'name': 'Nadezhda Kosintseva', 'rating': 2528, 'title': 8},
                        {'name': 'Tatiana Kosintseva', 'rating': 2532, 'title': 8},
                        {'name': 'Viktorija Cmilyte', 'rating': 2508, 'title': 8},
                       ]

    def find_player(self, name, list=None):
        if list is None:
            list = self.players
        for player in list:
            if player['name'] == name:
                return player
            
        return None

    def test_pairing_for_first_round(self):
        """
        Tests ordering by rating, title, name and simple pairing.
        """
        
        # Test name ordering
        players = [
                    {'name': 'Ad', 'rating': 0, 'title': 0},
                    {'name': 'Aa', 'rating': 0, 'title': 0},
                    {'name': 'Ab', 'rating': 0, 'title': 0},
                    {'name': 'Ac', 'rating': 0, 'title': 0},
                   ]
        pairing = Pairing(players)
        pairs = pairing.make_it()
        
        self.assertIn(self.find_player('Aa', players), pairs[0])
        self.assertIn(self.find_player('Ac', players), pairs[0])

        self.assertIn(self.find_player('Ab', players), pairs[1])
        self.assertIn(self.find_player('Ad', players), pairs[1])

        
        # Test rating and title ordering
        pairing = Pairing(self.players)
        pairs = pairing.make_it()
        
        self.assertIn(self.find_player('Hou Yifan'), pairs[0])
        self.assertIn(self.find_player('Antoaneta Stefanova'), pairs[0])

        self.assertIn(self.find_player('Anna Muzychuk'), pairs[1])
        self.assertIn(self.find_player('Viktorija Cmilyte'), pairs[1])

        self.assertIn(self.find_player('Humpy Koneru'), pairs[2])
        self.assertIn(self.find_player('Elina Danielian'), pairs[2])
        
        self.assertIn(self.find_player('Kateryna Lahno'), pairs[3])
        self.assertIn(self.find_player('Alisa Galliamova'), pairs[3])
        
        self.assertIn(self.find_player('Tatiana Kosintseva'), pairs[4])
        self.assertIn(self.find_player('Alexandra Kosteniuk'), pairs[4])

        self.assertIn(self.find_player('Nadezhda Kosintseva'), pairs[5])
        self.assertIn(self.find_player('Betul Cemre Yildiz'), pairs[5])
        
