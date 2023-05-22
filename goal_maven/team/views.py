"""
Views for the team APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from goal_maven.core.models import Team
# from goal_maven.core import models
from goal_maven.team import serializers
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from django.utils.translation import gettext_lazy as _

# import pdb


class TeamViewSet(viewsets.ModelViewSet):
    """View for manage team APIs."""
    serializer_class = serializers.TeamDetailSerializer
    queryset = Team.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Retrieve Teams for authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-id')

    def create(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.validate_staff(request)
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.TeamSerializer

        return self.serializer_class

    def validate_staff(self, request):
        """Validates if user is staff to make modification request."""
        if not request.user.is_staff:
            raise PermissionDenied(
                _("You don't have permission to perform this action.")
            )


class TeamStatsView(generics.GenericAPIView):
    """View for returning goals of a team."""
    serializer_class = serializers.TeamStatsSerializer

    def get(self, request, *args, **kwargs):

        team = get_object_or_404(Team, pk=kwargs.get('pk'))
        serializer = self.get_serializer(
            team,
            context={'season_name': kwargs.get('season_name')},
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
