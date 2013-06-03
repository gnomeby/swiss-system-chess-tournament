from django.views import generic
from tournaments.models import Tournament, Round, Game, Tournament_Player_Score
from django.shortcuts import get_object_or_404, render

class IndexView(generic.ListView):
    template_name = 'tournaments/index.html'
    context_object_name = 'tournaments_list'

    def get_queryset(self):
        return Tournament.objects.order_by('-start_date')
    
    
def details(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    players = tournament.players.order_by('name')
    return render(request, 'tournaments/details.html', {
                                                       'tournament': tournament,
                                                       'players': players,                                                       
                                                       })
    

def rounds(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    rounds = Round.objects.filter(tournament=pk).order_by('round_date')
    games = Game.objects.filter(round__tournament=pk).order_by('round__round_date')
    players = tournament.players.order_by('name')
    
    rounds_info = []
    for rnd in rounds:
        rounds_info.append({'round': rnd, 'games': []})
    for game in games:
        info = next(info for info in rounds_info if info['round'].id == game.round_id)
        info['games'].append({'game': game,
                              'player': find_player(game.player_id, players),
                              'opponent': find_player(game.opponent_id, players)
                              })
        
    return render(request, 'tournaments/rounds.html', {
                                                       'tournament': tournament,
                                                       'rounds_info': rounds_info,
                                                       })


def standings(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    scores = Tournament_Player_Score.objects
    rounds = Round.objects.filter(tournament=pk).order_by('round_date')
    player_scores = scores.filter(tournament=tournament).order_by(
                                                                  '-score',
                                                                  '-rating',
                                                                  '-fide_title',
                                                                  'name',
                                                                  )    
    games = Game.objects.filter(round__tournament=pk).order_by('round__round_date')
    players = tournament.players.order_by('name')
    
    players_info = []
    for player_score in player_scores:
        players_info.append({'player': find_player(player_score.player_id, players),
                             'games': [],
                             'score': player_score.score
                             })
    for game in games:
        info = next(info for info in players_info if info['player'].id == game.player_id)
        info['games'].append({'game': game,
                                  'player': find_player(game.player_id, players),
                                  'opponent': find_player(game.opponent_id, players)
                                  })
        info = next((info for info in players_info if info['player'].id == game.opponent_id), None)
        if info:
            info['games'].append({'game': game,
                                  'player': find_player(game.player_id, players),
                                  'opponent': find_player(game.opponent_id, players)
                                  })
    
    
    return render(request, 'tournaments/standings.html', {
                                                       'tournament': tournament,
                                                       'rounds': rounds,
                                                       'players_info': players_info,
                                                       })

    
def find_player(player_id, players):
    return next((player for player in players if player.id == player_id), None)
    