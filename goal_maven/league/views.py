"""
Views for the league APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from goal_maven.core.models import League, Season, LeagueTable
from goal_maven.league import serializers
from django.core.exceptions import PermissionDenied
# from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import generics

from django.utils.translation import gettext_lazy as _

# import pdb


class BaseView(viewsets.ModelViewSet):
    """BaseView containing common fields and methods."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Retrieve Leagues/league tables for requested season."""
    #     return self.queryset.filter(season=self.get_season())

    def list(self, request, *args, **kwargs):
        season = Season.objects.get(
            season_name=self.kwargs.get('season_name'),
        )
        queryset = self.get_queryset().filter(season=season)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def validate_staff(self, request):
        """Validates if user is staff to make modification request."""
        if not request.user.is_staff:
            raise PermissionDenied(
                _("You don't have permission to perform this action.")
            )


class LeagueViewSet(BaseView):
    """View for manage league APIs."""
    serializer_class = serializers.LeagueDetailSerializer
    queryset = League.objects.all()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.LeagueSerializer

        return self.serializer_class


class LeagueTableViewSet(BaseView):
    """View for manage league table APIs."""
    serializer_class = serializers.LeagueTableDetailSerializer
    queryset = LeagueTable.objects.all()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.LeagueTableSerializer

        return self.serializer_class


class SeasonViewSet(BaseView):
    """View for manage Season APIs."""
    serializer_class = serializers.SeasonDetailSerializer
    queryset = Season.objects.all()

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.SeasonSerializer

        return self.serializer_class
