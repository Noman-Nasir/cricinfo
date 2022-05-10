from django.urls import path
from rest_framework import routers

from series import views

urlpatterns = [
    path('stats/ground-stats', views.get_ground_with_most_matches, name='ground-stats'),
]
router = routers.SimpleRouter()
router.register(r'matches', views.MatchViewSet)
router.register(r'grounds', views.GroundViewSet)
router.register(r'series', views.SeriesViewSet)
urlpatterns += router.urls
