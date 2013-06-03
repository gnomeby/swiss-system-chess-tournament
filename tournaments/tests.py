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
        self.games = []

    def find_player(self, name, list=None):
        if list is None:
            list = self.players
        for player in list:
            if player['name'] == name:
                return player
            
        return None
    
    def fill_first_round_results(self):
        self.games.append({'player': 'Hou Yifan', 'opponent': 'Antoaneta Stefanova',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 1, 'is_walkover': False})

        self.games.append({'player': 'Anna Muzychuk', 'opponent': 'Viktorija Cmilyte',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'B', 'opponent_color': 'W',
                           'round': 1, 'is_walkover': False})

        self.games.append({'player': 'Humpy Koneru', 'opponent': 'Elina Danielian',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'B', 'opponent_color': 'W',
                           'round': 1, 'is_walkover': False})

        self.games.append({'player': 'Kateryna Lahno', 'opponent': 'Alisa Galliamova',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'B', 'opponent_color': 'W',
                           'round': 1, 'is_walkover': False})

        self.games.append({'player': 'Tatiana Kosintseva', 'opponent': 'Alexandra Kosteniuk',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 1, 'is_walkover': False})

        self.games.append({'player': 'Nadezhda Kosintseva', 'opponent': 'Betul Cemre Yildiz',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'B', 'opponent_color': 'W',
                           'round': 1, 'is_walkover': False})
        pass
    
    def fill_second_round_results(self):
        self.games.append({'player': 'Kateryna Lahno', 'opponent': 'Hou Yifan',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 2, 'is_walkover': False})

        self.games.append({'player': 'Anna Muzychuk', 'opponent': 'Elina Danielian',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 2, 'is_walkover': False})

        self.games.append({'player': 'Humpy Koneru', 'opponent': 'Viktorija Cmilyte',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 2, 'is_walkover': False})

        self.games.append({'player': 'Tatiana Kosintseva', 'opponent': 'Betul Cemre Yildiz',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 2, 'is_walkover': False})

        self.games.append({'player': 'Nadezhda Kosintseva', 'opponent': 'Alexandra Kosteniuk',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 2, 'is_walkover': False})

        self.games.append({'player': 'Antoaneta Stefanova', 'opponent': 'Alisa Galliamova',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 2, 'is_walkover': False})

        pass
    
    def fill_third_round_results(self):
        self.games.append({'player': 'Hou Yifan', 'opponent': 'Tatiana Kosintseva',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 3, 'is_walkover': False})

        self.games.append({'player': 'Kateryna Lahno', 'opponent': 'Nadezhda Kosintseva',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 3, 'is_walkover': False})

        self.games.append({'player': 'Elina Danielian', 'opponent': 'Viktorija Cmilyte',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 3, 'is_walkover': False})

        self.games.append({'player': 'Humpy Koneru', 'opponent': 'Anna Muzychuk',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 3, 'is_walkover': False})

        self.games.append({'player': 'Alexandra Kosteniuk', 'opponent': 'Antoaneta Stefanova',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 3, 'is_walkover': False})

        self.games.append({'player': 'Alisa Galliamova', 'opponent': 'Betul Cemre Yildiz',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 3, 'is_walkover': False})

        pass

    def fill_fourth_round_results(self):
        
        self.games.append({'player': 'Nadezhda Kosintseva', 'opponent': 'Hou Yifan',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 4, 'is_walkover': False})

        self.games.append({'player': 'Anna Muzychuk', 'opponent': 'Kateryna Lahno',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'B', 'opponent_color': 'W',
                           'round': 4, 'is_walkover': False})

        self.games.append({'player': 'Humpy Koneru', 'opponent': 'Alisa Galliamova',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 4, 'is_walkover': False})

        self.games.append({'player': 'Tatiana Kosintseva', 'opponent': 'Elina Danielian',
                           'player_score': 0.0, 'opponent_score': 1.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 4, 'is_walkover': False})

        self.games.append({'player': 'Viktorija Cmilyte', 'opponent': 'Antoaneta Stefanova',
                           'player_score': 0.5, 'opponent_score': 0.5,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 4, 'is_walkover': False})

        self.games.append({'player': 'Alexandra Kosteniuk', 'opponent': 'Betul Cemre Yildiz',
                           'player_score': 1.0, 'opponent_score': 0.0,
                           'player_color': 'W', 'opponent_color': 'B',
                           'round': 4, 'is_walkover': False})

        pass
    
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

        
    def test_pairing_for_second_round(self):
        """
        Tests ordering by score, rating, title, name and pairing including transposition.
        """
        
        self.fill_first_round_results()
        
        pairing = Pairing(self.players, self.games, 2)
        pairs = pairing.make_it()
        
        # Check pairs and color
        self.assertEqual(self.find_player('Kateryna Lahno'), pairs[0][0])
        self.assertEqual(self.find_player('Hou Yifan'), pairs[0][1])

        self.assertEqual(self.find_player('Anna Muzychuk'), pairs[1][0])
        self.assertEqual(self.find_player('Elina Danielian'), pairs[1][1])

        self.assertEqual(self.find_player('Humpy Koneru'), pairs[2][0])
        self.assertEqual(self.find_player('Viktorija Cmilyte'), pairs[2][1])

        self.assertEqual(self.find_player('Tatiana Kosintseva'), pairs[3][0])
        self.assertEqual(self.find_player('Betul Cemre Yildiz'), pairs[3][1])

        self.assertEqual(self.find_player('Nadezhda Kosintseva'), pairs[4][0])
        self.assertEqual(self.find_player('Alexandra Kosteniuk'), pairs[4][1])

        self.assertEqual(self.find_player('Antoaneta Stefanova'), pairs[5][0])
        self.assertEqual(self.find_player('Alisa Galliamova'), pairs[5][1])

        pass
    
    def test_pairing_for_third_round(self):
        """
        Tests ordering by score, rating, title, name and pairing including transposition.
        """
        
        self.fill_first_round_results()
        self.fill_second_round_results()

        pairing = Pairing(self.players, self.games, 3)
        pairs = pairing.make_it()
        
        # Check pairs and color
        self.assertEqual(self.find_player('Hou Yifan'), pairs[0][0])
        self.assertEqual(self.find_player('Tatiana Kosintseva'), pairs[0][1])

        self.assertEqual(self.find_player('Kateryna Lahno'), pairs[1][0])
        self.assertEqual(self.find_player('Nadezhda Kosintseva'), pairs[1][1])

        self.assertEqual(self.find_player('Viktorija Cmilyte'), pairs[2][0])
        self.assertEqual(self.find_player('Elina Danielian'), pairs[2][1])

        self.assertEqual(self.find_player('Anna Muzychuk'), pairs[3][0])
        self.assertEqual(self.find_player('Humpy Koneru'), pairs[3][1])

        self.assertEqual(self.find_player('Alexandra Kosteniuk'), pairs[4][0])
        self.assertEqual(self.find_player('Antoaneta Stefanova'), pairs[4][1])

        self.assertEqual(self.find_player('Alisa Galliamova'), pairs[5][0])
        self.assertEqual(self.find_player('Betul Cemre Yildiz'), pairs[5][1])

        pass
    
    def test_pairing_for_fourth_round(self):
        """
        Tests ordering by score, rating, title, name and pairing including transposition.
        """
        
        self.fill_first_round_results()
        self.fill_second_round_results()
        self.fill_third_round_results()

        pairing = Pairing(self.players, self.games, 4)
        pairs = pairing.make_it()
        
        # Check pairs and color
        self.assertEqual(self.find_player('Nadezhda Kosintseva'), pairs[0][0])
        self.assertEqual(self.find_player('Hou Yifan'), pairs[0][1])

        self.assertEqual(self.find_player('Anna Muzychuk'), pairs[1][0])
        self.assertEqual(self.find_player('Kateryna Lahno'), pairs[1][1])

        self.assertEqual(self.find_player('Humpy Koneru'), pairs[2][0])
        self.assertEqual(self.find_player('Alisa Galliamova'), pairs[2][1])

        self.assertEqual(self.find_player('Tatiana Kosintseva'), pairs[3][0])
        self.assertEqual(self.find_player('Elina Danielian'), pairs[3][1])

        self.assertEqual(self.find_player('Viktorija Cmilyte'), pairs[4][0])
        self.assertEqual(self.find_player('Antoaneta Stefanova'), pairs[4][1])

        self.assertEqual(self.find_player('Alexandra Kosteniuk'), pairs[5][0])
        self.assertEqual(self.find_player('Betul Cemre Yildiz'), pairs[5][1])

        pass
    
    def test_pairing_for_fifth_round(self):
        """
        Tests ordering by score, rating, title, name and pairing including transposition.
        """

        self.fill_first_round_results()
        self.fill_second_round_results()
        self.fill_third_round_results()
        self.fill_fourth_round_results()
        
        pairing = Pairing(self.players, self.games, 4)
        pairs = pairing.make_it()
        print pairs
        
        # Check pairs and color
        self.assertEqual(self.find_player('Hou Yifan'), pairs[0][0])
        self.assertEqual(self.find_player('Humpy Koneru'), pairs[0][1])

        self.assertEqual(self.find_player('Elina Danielian'), pairs[1][0])
        self.assertEqual(self.find_player('Kateryna Lahno'), pairs[1][1])

        self.assertEqual(self.find_player('Anna Muzychuk'), pairs[2][0])
        self.assertEqual(self.find_player('Nadezhda Kosintseva'), pairs[2][1])

        self.assertEqual(self.find_player('Viktorija Cmilyte'), pairs[3][0])
        self.assertEqual(self.find_player('Alexandra Kosteniuk'), pairs[3][1])

        self.assertEqual(self.find_player('Alisa Galliamova'), pairs[4][0])
        self.assertEqual(self.find_player('Tatiana Kosintseva'), pairs[4][1])

        self.assertEqual(self.find_player('Betul Cemre Yildiz'), pairs[5][0])
        self.assertEqual(self.find_player('Antoaneta Stefanova'), pairs[5][1])

        pass
        