"""
URL mappings for the league app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from goal_maven.league import views

# import pdb


router = DefaultRouter()
router.register('leagues', views.LeagueViewSet, basename='league')
router.register('league-tables', views.LeagueTableViewSet, basename='league-table')
router.register('seasons', views.SeasonViewSet, basename='season')

app_name = 'league'

urlpatterns = [
    path('', include(router.urls)),
    path('/<str:season_name>/', include(router.urls)),
]
