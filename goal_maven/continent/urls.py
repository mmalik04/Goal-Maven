"""
URL mappings for the continent app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from goal_maven.continent import views

# import pdb


router = DefaultRouter()
router.register('continents', views.ContinentViewSet)

app_name = 'continent'

urlpatterns = [
    path('', include(router.urls)),
]
# pdb.set_trace()
