from django.views import generic
from tournaments.models import Tournament, Round, Game, Tournament_Player_Score
from django.shortcuts import get_object_or_404, render

class IndexView(generic.ListView):
    template_name = 'tournaments/index.html'
    context_object_name = 'tournaments_list'

    def get_queryset(self):
        return Tournament.objects.order_by('-start_date')
    
    
class DetailView(generic.DetailView):
    model = Tournament
    template_name = 'tournaments/detail.html'
    

class PlayersView(generic.DetailView):
    model = Tournament
    template_name = 'tournaments/players.html'

    
def rounds(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    rounds = Round.objects.filter(tournament=pk)
    games = Game.objects.filter(round__tournament=pk)
    return render(request, 'tournaments/rounds.html', {
                                                       'tournament': tournament,
                                                       'rounds': rounds,
                                                       'games': games,                                                       
                                                       })


def standings(request, pk):
    tournament = get_object_or_404(Tournament, pk=pk)
    scores = Tournament_Player_Score.objects
    player_scores = scores.filter(tournament=tournament).order_by(
                                                                  '-score',
                                                                  '-rating',
                                                                  '-title_number',
                                                                  'name',
                                                                  )    
    rounds = Round.objects.filter(tournament=pk)
    games = Game.objects.filter(round__tournament=pk)
    return render(request, 'tournaments/standings.html', {
                                                       'tournament': tournament,
                                                       'player_scores': player_scores,
                                                       'rounds': rounds,
                                                       'games': games,                                                       
                                                       })    