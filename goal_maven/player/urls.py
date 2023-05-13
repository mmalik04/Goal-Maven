"""
URL mappings for the player app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from goal_maven.player import views

# import pdb


router = DefaultRouter()
router.register('players', views.PlayerViewSet)

app_name = 'player'

urlpatterns = [
    path('', include(router.urls)),
]
