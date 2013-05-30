from django.contrib import admin
from django import forms
from tournaments.models import Player, Tournament


# Sort players alphabetically
class PlayerInlineForm(forms.ModelForm):
    player = forms.ModelChoiceField(queryset=Player.objects.order_by('name'))
    player.label = 'Player'
    
class PlayerInline(admin.TabularInline):
    model = Tournament.players.through
    form = PlayerInlineForm
    extra = 0

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'city', 'start_date', 'end_date', 'players_count', 'add_round_link')
    list_filter = ['start_date']
    date_hierarchy = 'start_date'
    search_fields = ['name']
    ordering = ['-start_date']
    inlines = [PlayerInline]
    exclude = ['players']
    admin.site.disable_action('delete_selected')
    class Media:
        css = { "all" : ("css/additional_admin.css",) }    
    
    def add_round_link(self, tour):
        return '{0:d}' \
               ' (<a href="../round/add?tournament={1:d}&name={2:s}">add new</a>,' \
               ' <a href="../round/?q={3:s}">list</a>' \
               ')'.format(
                            tour.round_set.count(), 
                            tour.id,
                            "Round " + str(tour.round_set.count() + 1),
                            tour.name
                            )
    add_round_link.short_description = 'Rounds'
    add_round_link.allow_tags = True    

admin.site.register(Tournament, TournamentAdmin)
