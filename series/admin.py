from django.contrib import admin
from .models import Match, Ground


class MatchInLine(admin.StackedInline):
    model = Match


class GroundAdmin(admin.ModelAdmin):
    model = Ground
    inlines = [
        MatchInLine
    ]


admin.site.register(Ground, GroundAdmin)
admin.site.register(Match)
