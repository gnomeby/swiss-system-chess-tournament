import math

def pair_ordered_players(player_tuples, games):
    S1 = [] 
    S2 = []

    current_group = []
    prev_score = None
    for (player, score) in player_tuples:
        if len(current_group) < 2 or prev_score == score:
            current_group.append(player)
        else:
            # Pairing
            if len(current_group) % 2 == 0:
                pair_players_into_S_arrays(current_group, S1, S2)
                current_group = []
            else:
                pair_players_into_S_arrays(current_group[:-1], S1, S2)
                current_group = current_group[-1:]
                
            current_group.append(player)
        prev_score = score
    if len(current_group) > 0:
        pair_players_into_S_arrays(current_group, S1, S2)
    
    print S1
    print S2
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
