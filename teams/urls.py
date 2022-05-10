from django.urls import path
from rest_framework import routers

from teams import views

urlpatterns = [
    path('stats/player-visits', views.get_most_visited_player, name='player-visits'),
    path('stats/player-type-stats', views.get_player_stats_based_on_type, name='player-type-visits'),
]
router = routers.SimpleRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'teams', views.TeamViewSet)
urlpatterns += router.urls
