from django.contrib import admin
from django.db.models import Q
from tournaments.models import Player, Tournament, Game
from datetime import date
from tournaments import rating_elo

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'country', 'fide_id', 'fide_title', 'rating', 'rating_dev_coef')
        }),
    )
    list_display = ('name', 'fide_title', 'country', 'rating', 'fide_id', 
                    'register_date', 'last_rating_calculation')
    search_fields = ['name'],
    ordering = ['name']
    actions = ['recalculate_rating']
    
    def recalculate_rating(self, request, queryset):
        for player in queryset:
            games_in_past_events = 0
            
            if player.last_rating_calculation:
                # Calculate games_in_past_events
                if player.rating_dev_coef is None:
                    tour_player = Tournament.players.through.objects.filter(
                                player=player,
                                tournament__end_date__let=player.last_rating_calculation
                                ).order_by('tournament__start_date')
                    
                    for link in tour_player:
                        games = Game.objects.filter(Q(player=player) | Q(opponent=player),
                                                    status='finished',
                                                    round__tournament=link.tournament)
                        games_in_past_events += games.count()
                    pass
                tour_player = Tournament.players.through.objects.filter(
                            player=player,
                            tournament__end_date__lt=date.today(),
                            tournament__end_date__gt=player.last_rating_calculation
                            ).order_by('tournament__start_date')
            else:
                tour_player = Tournament.players.through.objects.filter(
                            player=player,
                            tournament__end_date__lt=date.today()
                            ).order_by('tournament__start_date')
            
            for link in tour_player:
                games = Game.objects.filter(Q(player=player) | Q(opponent=player),
                                            status='finished',
                                            round__tournament=link.tournament)
                delta_rating = 0.0
                if player.rating_dev_coef:
                    k = player.rating_dev_coef
                else:
                    k = rating_elo.calculate_k(player.rating, games_in_past_events)
                    if k == 10:
                        player.rating_dev_coef = k

                for game in games:
                    score = game.player_score if game.player == player else game.opponent_score
                    opponent = game.opponent if game.player == player else game.player
                    
                    delta_rating += rating_elo.calculate_delta(player.rating, opponent.rating, score, k)
                    
                games_in_past_events += games.count()
                player.rating = round(player.rating + delta_rating)
                player.last_rating_calculation = link.tournament.end_date
                
            if player.save():
                self.message_user(request, "%s rating was recalculated." % player)
            else:
                self.message_user(request, "%s rating remains the same." % player)
    
admin.site.register(Player, PlayerAdmin)