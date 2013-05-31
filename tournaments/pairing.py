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
        
        # Apply game results
        sorted_games = sorted(self.games, key=lambda game: game['name'])         
        for game in sorted_games:
            info = player_info[game['player']]
            info['score'] += game['player_score']
            #info['upfloats'] = game['player_score']
            # B.5, B.6
            info['floats'] += 'D' if game['player_score'] > 0 and game['is_walkover'] else '-'
            info['colors'] += 'W' if game['player_color'] == 'W' and game['is_walkover'] else 'B'
            
            if game['opponent'] is None:
                continue
            # B.1.a
            info['opponents'].append(game['opponent'])
            
            info = player_info[game['opponent']]
            info['score'] += game['opponent_score']
            info['floats'] += 'D' if game['opponent_score'] > 0 and game['is_walkover'] else '-'
            info['colors'] += 'B' if game['player_color'] == 'W' and game['is_walkover'] else 'W'
            
            info['opponents'].append(game['player'])
            
        self.player_info = player_info
        
        # A.3
        brackets = {}
        for player, info in player_info:
            if info['score'] not in brackets:
                brackets[info['score']] = []
            brackets[info['score']].append(player)
        self.brackets = brackets

        
    def make_it(self):
        if self.next_round == 1:
            self.pair_first_round()
            
        return self.pairs
    
    def pair_first_round(self):
        sorted_players = sorted(self.players, key=lambda player: player['name'])
        sorted_players = sorted(sorted_players, reverse=True, key=lambda player: player['title'])
        sorted_players = sorted(sorted_players, reverse=True, key=lambda player: player['rating'])
        S1 = len(self.players) / 2
        for index in range(S1):
            self.pairs.append([sorted_players[index], sorted_players[S1+index]])
        if len(self.players) % 2 == 1:
            self.pairs.append([sorted_players[S1*2+1], None])
        pass

# Implemented rules: B.1, B.5, B.6
def pair_ordered_players(player_scores, ordered_games, round_number):
    S1 = [] 
    S2 = []

    players = []
    player_info = {}
    for score_row in player_scores:
        players.append(score_row.player)
        player_info[score_row.player.id] = {'score': score_row.score,
                                            'upfloats': 0,      # B.6
                                            'downfloats': 0,    # B.6
                                            'prev_round_float': 0,   # B.5
                                            'floats': ''
                                            }
        
    for player in players:        
        info = player_info[player.id]
        info['rating'] = player.rating
        info['title'] = int(player.fide_title[0])
        info['name'] = player.name
        info['color_pref'] = get_color_preference(player, ordered_games)
        info['possible_opponents'] = get_possible_opponents(player, players, ordered_games) # B.1.a
                
    for game in ordered_games:
        # B.1.b
        if game.status == 'walkover':
            player_id = game.player.id if game.player_score > 0.0 else game.opponent.id
            player_info[player_id]['downfloats'] += 1            # B.1.b, B.6
            player_info[player_id]['is_bye_allowed'] = False     # B.1.b
            player_info[player_id]['prev_round_float'] = 'down'  # B.5
        else:
            player_info[game.player.id]['prev_round_float'] = None
            if game.opponent:
                player_info[game.opponent.id]['prev_round_float'] = None
            pass            
            
    # A.3
    brackets = {}
    for player_id, info in player_info:
        if info['score'] not in brackets:
            brackets[info['score']] = []
        brackets[info['score']].append(player_id)

    # C
    for score in sorted(brackets, reversed=True):
        # C.1
        problems = find_players_without_opponents(brackets[score])
        pass                 
    current_group = []
    prev_score = None
    for score_row in player_scores:
        if len(current_group) < 2 or prev_score == score_row.score:
            current_group.append(score_row.player)
        else:
            # Pairing
            if len(current_group) % 2 == 0:
                pair_players_into_S_arrays(current_group, S1, S2)
                current_group = []
            else:
                pair_players_into_S_arrays(current_group[:-1], S1, S2)
                current_group = current_group[-1:]
                
            current_group.append(score_row.player)
        prev_score = score_row.score
    if len(current_group) > 0:
        pair_players_into_S_arrays(current_group, S1, S2)
    
    return S1 + S2

def pair_players_into_S_arrays(players, S1, S2):
    half = int(math.ceil(float(len(players)) / 2.0))
    i = 0
    for player in players[:half]:
        opponent = players[half + i] if half + i < len(players) else None 
        S1.append(player)
        S2.append(opponent)
        i+=1
    pass

def get_color_preference(player, games):
    preference = 0
    for game in games:
        if game.player == player and game.status == 'finished':
            preference += 1 if game.player_color == "W" else -1
        if game.opponent == player and game.status == 'finished':
            preference += 1 if game.opponent_color == "W" else -1
            
    return preference

# B - Pairing Criteria
# Absolute Criterias
# B.1.a 
def get_possible_opponents(player, players, games):
    opponents = players[:]
    opponents.remove(player)
    for game in games:
        if game.player == player and game.opponent is not None:
            opponents.remove(game.opponent)
        if game.opponent == player:
            opponents.remove(game.player)
                
    return opponents

# C.1
def find_players_without_opponents(bracket):
    for player_id in bracket:
        pass
    pass