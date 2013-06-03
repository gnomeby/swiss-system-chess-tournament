import math

class Pairing:
    '''Pairing procedure according to Swiss system rules'''
    
    def __init__(self, players, games=[], next_round=1):
        ''' players - list of dicts(name, rating, title)
        games - list of dicts(round, player(name), opponent(name||None), player_score, opponent_score, player_color, opponent_color, is_walkover)
        round_number - number of next round
        '''
        self.pairs = []
        self.players = players
        self.games = games
        self.next_round = next_round

        # Collect player info
        initial_info = {'score': 0, 'floats': '', 'colors': ''}
        player_info = {player['name']:initial_info.copy() for player in players}
        for player in players:        
            info = player_info[player['name']]
            info['rating'] = player['rating']
            info['title'] = player['title']
            info['name'] = player['name']
            info['opponents'] = []
        
        # Apply game results
        sorted_games = sorted(self.games, key=lambda game: game['round'])         
        for game in sorted_games:
            info = player_info[game['player']]
            info['score'] += game['player_score']
            #info['upfloats'] = game['player_score']
            # B.5, B.6
            info['floats'] += 'D' if game['player_score'] > 0 and game['is_walkover'] else '-'
            if game['is_walkover'] is False:
                info['colors'] += 'W' if game['player_color'] == 'W' else 'B'
            
            if game['opponent'] is None:
                continue
            # B.1.a
            info['opponents'].append(self.find_player_by_name(game['opponent']))
            
            info = player_info[game['opponent']]
            info['score'] += game['opponent_score']
            info['floats'] += 'D' if game['opponent_score'] > 0 and game['is_walkover'] else '-'
            if game['is_walkover'] is False:
                info['colors'] += 'W' if game['opponent_color'] == 'W' else 'B'
            
            info['opponents'].append(self.find_player_by_name(game['player']))
            
        self.player_info = player_info
        
        # A.3
        brackets = {}
        for player_name, info in self.player_info.iteritems():
            if info['score'] not in brackets:
                brackets[info['score']] = []
            brackets[info['score']].append(self.find_player_by_name(player_name))
        self.brackets = brackets

        
    def make_it(self):
        if self.next_round == 1:
            self.pair_first_round()
        elif self.next_round % 2 == 0:
            self.pair_even_round()
        elif self.next_round % 2 == 1:
            self.pair_odd_round()
            
        return self.pairs
    
    def order_players(self, players):
        sorted_players = sorted(players, key=lambda player: player['name'])
        sorted_players = sorted(sorted_players, reverse=True, key=lambda player: player['title'])
        sorted_players = sorted(sorted_players, reverse=True, key=lambda player: player['rating'])
        sorted_players = sorted(sorted_players, reverse=True, key=lambda player: self.player_info[player['name']]['score'])
        return sorted_players
        
    def pair_first_round(self):
        sorted_players = self.order_players(self.players)
        S1count = len(self.players) / 2
        for index in range(S1count):
            self.pairs.append([sorted_players[index], sorted_players[S1count+index]])
        if len(self.players) % 2 == 1:
            self.pairs.append([sorted_players[S1count*2+1], None])
        pass
    
    def pair_odd_round(self):
        self.pair_even_round()
        
    def pair_even_round(self):
        sorted_brackets_keys = sorted(self.brackets, reverse=True)
        highest_group = sorted_brackets_keys[0]
        lowest_group = sorted_brackets_keys[-1:]
        downfloaters = []

        for group_score in sorted_brackets_keys:
            group = self.brackets[group_score]
            if len(downfloaters) > 0:
                # TODO: B.5, B.6
                group[0:0] = downfloaters
                
                
            downfloaters = []
            for player in group:
                if player.has_key('pair') and player['pair']:
                    continue
                
                opponents = self.find_possible_opponents(player, group)
                
                # C.1: B.1, B.2
                if len(opponents) == 0:
                    player['downfloater'] = True
                    downfloaters.append(player)
                elif len(opponents) == 1:
                    if player.has_key('downfloater') and player['downfloater']:
                        opponents[0]['upfloater'] = True
                    playerW, playerB = self.return_with_color_preferences(player, opponents[0])
                    self.pairs.append([playerW, playerB])
                    playerW['pair'] = True
                    playerB['pair'] = True
                elif len(opponents) > 1 and player.has_key('downfloater') and player['downfloater']:
                    sorted_players = self.order_players(opponents)
                    sorted_players[0]['upfloater'] = True
                    playerW, playerB = self.return_with_color_preferences(player, sorted_players[0])
                    self.pairs.append([playerW, playerB])
                    playerW['pair'] = True
                    playerB['pair'] = True
                    pass
                    
            without_opponents = [pl for pl in group if not pl.has_key('pair') or pl['pair'] is False]
            if len(without_opponents) > 2:
                self.pair_group_with_transposition(without_opponents)
                without_opponents = [pl for pl in group if not pl.has_key('pair') or pl['pair'] is False]
                if len(without_opponents) == 1:
                    without_opponents[0]['downfloater'] = True
                    downfloaters.append(without_opponents[0])
            
            if len(downfloaters) > 0 and lowest_group == group_score:
                pass
        pass
    
    # D 1.1 Homogenius transposition
    def pair_group_with_transposition(self, group):
        sorted_players = self.order_players(group)
        S1count = len(sorted_players) / 2
        S2count = len(sorted_players) - S1count
        S1 = sorted_players[:S1count]
        S2 = sorted_players[S1count:]

        def transposition(k,n):
            if k == n:
                yield S2
            else:
                for i in range(k, n):
                    if i != k:
                        S2[k], S2[i] = S2[i], S2[k]
                    for x in transposition(k+1, n):
                        yield x
                    if i != k:
                        S2[k], S2[i] = S2[i], S2[k]
            pass

        # Check simple pairing
        for S2 in transposition(0, S2count):
            problems = 0
            for index in range(S1count):
                if S2[index] not in self.find_possible_opponents(S1[index], group):
                    problems += 1
                    break
                    
            if problems > 0:
                continue
            
            # Pairing
            for index in range(S1count):
                playerW, playerB = self.return_with_color_preferences(S1[index], S2[index])
                self.pairs.append([playerW, playerB])
                playerW['pair'] = True
                playerB['pair'] = True
                
            return group
                
        return group
    
    def return_with_color_preferences(self, playerA, playerB):
        player1, player2 = self.order_players([playerA, playerB])
        player1_pref = self.get_color_preferences(player1)
        player2_pref = self.get_color_preferences(player2)
        player1_switched_color = self.get_switched_color_for_latest_game(player1)
        player2_switched_color = self.get_switched_color_for_latest_game(player2)
        
        if player1_pref <= -2 or player2_pref >= 2:
            return player1, player2
        elif player1_pref == -1 or player2_pref == 1:
            return player1, player2
        elif player1_pref >= 2 or player2_pref <= -2:
            return player2, player1
        elif player1_pref == 1 or player2_pref == -1:
            return player2, player1
        elif player1_switched_color and player1_switched_color == 'W':
            return player1, player2
        elif player2_switched_color and player2_switched_color == 'W':
            return player2, player1
        
        return player1, player2
    
    def find_player_by_name(self, name):
        for player in self.players:
            if player['name'] == name:
                return player
        return None

    # B.1, B.2    
    def find_possible_opponents(self, current_player, group, skip_color_pref = False):
        info = self.player_info[current_player['name']]
        rest = [player for player in group if current_player != player]
        rest = [player for player in rest if player not in info['opponents']]   # B.1
        rest = [player for player in rest if not player.has_key('pair') or player['pair'] is False]
        if len(rest) == 0:
            return []
        
        # B.2
        # TODO: Top scored players
        color_pref = self.get_color_preferences(current_player)
        if abs(color_pref) >= 2 and skip_color_pref is False:
            for player in rest:
                opponent_color_pref = self.get_color_preferences(player)
                if opponent_color_pref == color_pref:
                    rest.remove(player)
                    continue
                 
        return rest
    
    def get_color_preferences(self, player):
        colors = self.player_info[player['name']]['colors']
        preference = 0
        for c in colors: preference += 1 if c == "W" else -1
        return preference
    
    def get_switched_color_for_latest_game(self, player):
        colors = self.player_info[player['name']]['colors']
        if len(colors) == 0:
            return None 
        return "W" if colors[-1:] == "B" else "B"

