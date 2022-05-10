from django.contrib import admin
from .models import Team


class PlayerInline(admin.TabularInline):
    model = Team.players.through


class TeamAdmin(admin.ModelAdmin):
    model = Team
    inlines = [
        PlayerInline
    ]


admin.site.register(Team, TeamAdmin)
