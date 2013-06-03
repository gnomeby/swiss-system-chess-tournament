import math


def calculate_delta(rating, opponent_rating, score, k):
    Ea = 1.0 / (1 + math.pow(10, (opponent_rating - rating) / 400))
    
    return k * (float(score) - Ea) 


def calculate_k(rating, past_event_games):
    if rating >= 2400.0 and past_event_games >= 30:
        k = 10
    elif rating < 2400.0 and past_event_games >= 30:
        k = 15
    else:
        k = 30

    return k