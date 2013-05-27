from django.contrib import admin
from tournaments.models import Player

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