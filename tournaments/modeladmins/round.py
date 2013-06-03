from django.contrib import admin
from django import forms
from tournaments.models import Player, Tournament, Game, Round
import math
from django.utils.functional import curry
import re
from tournaments.pairing import Pairing


class GameInLineFormAdmin(forms.ModelForm):
    player = forms.ModelChoiceField(queryset=Player.objects.order_by('name'))
    player.label = 'Player'
    opponent = forms.ModelChoiceField(queryset=Player.objects.order_by('name'), required=False)
    opponent.label = 'Opponent'
    
    def __init__(self, *args, **kwargs):
        super(GameInLineFormAdmin, self).__init__(*args, **kwargs)
        
        initial = kwargs.get('initial', None)
        game = kwargs.get('instance', None)
        if game:
            self.fields['player'].queryset = game.round.tournament.players.order_by('name')
            self.fields['opponent'].queryset = game.round.tournament.players.order_by('name')
        elif initial and initial.has_key('tournament'):
            self.fields['player'].queryset = initial['tournament'].players.order_by('name')
            self.fields['opponent'].queryset = initial['tournament'].players.order_by('name')
    
    def clean(self):
        cleaned_data = super(GameInLineFormAdmin, self).clean()
        tour = Tournament.objects.get(pk=self.data['tournament'])
        
        # Check players
        player = cleaned_data.get("player")
        opponent = cleaned_data.get("opponent") if cleaned_data.has_key("opponent") else None
        if player == opponent:
            self._errors["opponent"] = self.error_class([u'Player cannot play with oneself'])
            del cleaned_data["opponent"]

        if tour.players.filter(id=player.id).count() == 0:
            self._errors["player"] = self.error_class([u'%s is not in this tournament.' % player])
            del cleaned_data["player"]
            
        if opponent is not None and tour.players.filter(id=opponent.id).count() == 0:
            self._errors["opponent"] = self.error_class([u'%s is not in this tournament.' % opponent])
            del cleaned_data["opponent"]
            
        if tour.players.count() % 2 == 0 and opponent is None:
            self._errors["player"] = self.error_class([u'You cannot have games without opponent in tournament with even players count'])
            del cleaned_data["player"]

        if opponent is not None and len(self.data['round_date']) > 0:
            # See format in settings
            m = re.match('(?P<day>\d+).(?P<month>\d+).(?P<year>\d+)', self.data['round_date'])
            if m is not None:
                iso_date = "{0:s}-{1:s}-{2:s}".format(m.group('year'), m.group('month'), m.group('day'))
                games = Game.objects.filter(round__tournament=tour, 
                                            round__round_date__lt=iso_date
                                            )
                for game in games:
                    if (game.player == player and game.opponent == opponent) or \
                        (game.opponent == player and game.player == opponent):
                        self._errors["player"] = self.error_class([u'The same pair was in one of previous rounds'])
                        del cleaned_data["player"]
                        
        
        # Check colors
        player_color = cleaned_data.get("player_color")
        opponent_color = cleaned_data.get("opponent_color")

        if player_color != "W" and player_color != "B":
            self._errors["player_color"] = self.error_class([u'Player has incorrect color'])
            del cleaned_data["player_color"]
            
        if opponent_color != "W" and opponent_color != "B":
            self._errors["opponent_color"] = self.error_class([u'Opponent has incorrect color'])
            del cleaned_data["opponent_color"]
            
        if player_color == opponent_color:
            self._errors["opponent_color"] = self.error_class([u'Opponent must not have the same color'])
            del cleaned_data["opponent_color"]
        
        # Check score and status
        player_score = cleaned_data.get("player_score")
        opponent_score = cleaned_data.get("opponent_score")
        status = cleaned_data.get("status")
         
        total_score = float(player_score) + float(opponent_score)
        if status == 'planned' and total_score > 0:
            self._errors["status"] = self.error_class([u'Planned status is not allowed if game has score'])
            del cleaned_data["status"]
            
        elif status != 'planned' and total_score == 0:
            self._errors["status"] = self.error_class([u'Planned status must be set if game has not score'])
            del cleaned_data["status"]

        elif status != 'planned' and ((tour.bye_score == 1.0 and total_score == 0.5) or total_score > 1):
            self._errors["player_score"] = self.error_class([u'Incorrect total score'])
            self._errors["opponent_score"] = self._errors["player_score"] 
            del cleaned_data["player_score"]
            del cleaned_data["opponent_score"]
            
        return cleaned_data
            
class GameInline(admin.TabularInline):
    model = Game
    form = GameInLineFormAdmin
    extra = 0
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super(GameInline, self).get_formset(request, obj, **kwargs)
        
        initial = []
        
        if request.method == "GET" and obj is None and request.GET.has_key('tournament'):
            tournament = Tournament.objects.get(pk=request.GET['tournament'])
            
            if tournament.round_set.count() == 0:
                players = tournament.players.order_by('-rating', '-fide_title', 'name')
                half = int(math.ceil(float(len(players)) / 2.0))
                for i in range(half):
                    initial.append({'player': players[i],
                                    'opponent': players[half + i] if half + i < len(players) else None,
                                    'tournament': tournament})
                pass
            else:
                players = tournament.players.order_by('-rating', '-fide_title', 'name')
                players_list = [{ 
                                  'name': player.name, 
                                  'rating': player.rating,  
                                  'title': int(player.fide_title[:1]),
                                  'player': player
                                  }
                                for player in players
                                ]
                
                games = Game.objects.filter(round__tournament=tournament).order_by('round__round_date')
                games_list = [{'round': game.round.id, 
                              'player': game.player.name, 
                              'opponent': game.opponent.name if game.opponent else None,
                              'player_score': game.player_score,  
                              'opponent_score': game.opponent_score, 
                              'player_color': game.player_color,  
                              'opponent_color': game.opponent_color, 
                              'is_walkover': game.status == 'walkover'}
                              for game in games
                              ]
                pairing = Pairing(players_list, games_list, tournament.round_set.count() + 1)
                pairs = pairing.make_it()
                for pair in pairs:
                    initial.append({'player': pair[0]['player'],
                                    'opponent': pair[1]['player'],
                                    'tournament': tournament})

            
            formset.extra = len(initial)
        
        formset.__init__ = curry(formset.__init__, initial=initial)
        
        return formset

class RoundFormAdmin(forms.ModelForm):
    def clean(self):
        cleaned_data = super(RoundFormAdmin, self).clean()
        
        tour = cleaned_data.get("tournament")
        if tour is not None:
            if self.instance.pk is None and tour.round_set.count() > 0:
                prev_round = tour.round_set.order_by("-round_date")[0]
                if prev_round.game_set.count() == 0:
                    raise forms.ValidationError("The previous round doesn't have any games.")
                elif prev_round.game_set.filter(status="planned").count() > 0:
                    raise forms.ValidationError("The previous round has unfinished games.")

        return cleaned_data
            
    pass
    
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_tournament_link', 'round_date')
    list_filter = ['round_date']
    date_hierarchy = 'round_date'
    search_fields = ['tournament__name', 'name']
    ordering = ['-round_date']
    inlines = [GameInline]
    form = RoundFormAdmin
    
    class Media:
        css = { "all" : ("css/additional_admin.css",) }
             
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}
    
            
    def add_tournament_link(self, round):
        return '<a href="../tournament/?q={0:s}">{0:s}</a>'.format(round.tournament.name)
    add_tournament_link.short_description = 'Tournament'
    add_tournament_link.allow_tags = True    
    
admin.site.register(Round, RoundAdmin)
