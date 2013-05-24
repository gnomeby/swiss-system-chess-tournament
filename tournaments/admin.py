from django.contrib import admin
from tournaments.models import Player, Tournament, Round, Game

class PlayerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'country', 'fide_id', 'fide_title', 'initial_rating')
        }),
    )
    list_display = ('name', 'fide_title', 'country', 'rating', 'fide_id', 'register_date')
    search_fields = ['name'],
    ordering = ['name']
    
admin.site.register(Player, PlayerAdmin)


class PlayerInline(admin.TabularInline):
    model = Tournament.players.through
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
    
    def add_round_link(self, tour):
        return '{0:d} (<a href="../round/add' \
            '?tournament={1:d}&name={2:s}">add new</a>)'.format(
                                                                tour.round_set.count(), 
                                                                tour.id,
                                                                "Round " + str(tour.round_set.count() + 1)
                                                                )
    add_round_link.short_description = 'Rounds'
    add_round_link.allow_tags = True    

admin.site.register(Tournament, TournamentAdmin)


class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'tournament', 'round_date')
    list_filter = ['round_date']
    date_hierarchy = 'round_date'
    search_fields = ['name']
    ordering = ['-round_date']
    
admin.site.register(Round, RoundAdmin)


class GameAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'round', 'status')
    
admin.site.register(Game, GameAdmin)