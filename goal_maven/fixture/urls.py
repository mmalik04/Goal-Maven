"""
URL mappings for the fixture app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from goal_maven.fixture import views


router = DefaultRouter()
router.register('fixtures', views.FixtureViewSet)
router.register('matches', views.MatchViewSet)

app_name = 'fixture'

urlpatterns = [
    path('', include(router.urls)),
    path('<str:season_name>/', include(router.urls)),
    # path(
    #     'stats/<int:pk>/<str:season_name>/',
    #     views.TeamStatsView.as_view(),
    #     name='team-season-stats',
    # ),
]
