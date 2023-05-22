"""
URL mappings for the team app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from goal_maven.team import views


router = DefaultRouter()
router.register('teams', views.TeamViewSet)

app_name = 'team'

urlpatterns = [
    path('', include(router.urls)),
    path(
        'stats/<int:pk>/<str:season_name>/',
        views.TeamStatsView.as_view(),
        name='team-season-stats',
    ),
]
