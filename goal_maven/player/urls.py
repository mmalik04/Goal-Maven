"""
URL mappings for the player app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from goal_maven.player import views


router = DefaultRouter()
router.register('players', views.PlayerViewSet)

app_name = 'player'

urlpatterns = [
    path('', include(router.urls)),
    path(
        'stats/<int:pk>/<str:season_name>/',
        views.PlayerStatsView.as_view(),
        name='player-season-stats',
    ),
]
