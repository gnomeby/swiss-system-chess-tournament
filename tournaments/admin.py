from django.contrib import admin
from tournaments.models import Player, Tournament

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
    list_display = ('name', 'country', 'city', 'start_date', 'end_date')
    list_filter = ['start_date']
    date_hierarchy = 'start_date'
    search_fields = ['name']
    ordering = ['-start_date']
    inlines = [PlayerInline]
    exclude = ['players']

admin.site.register(Tournament, TournamentAdmin)